#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Command line App "framework".
'''

import sys
import csv
import signal
import logging
import logging.handlers
import argparse


def unicode_csv_reader(data, **kwargs):
    def utf_8_encoder(unicode_csv_data):
        for line in unicode_csv_data:
            yield line.decode('utf-8').encode('utf-8')
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(data), **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


class App(object):
    '''
    Create a def main() or several def action_foo()

    self.foreground() execute in foreground.
    self.run() run in foreground.
    '''

    @property
    def dryrun(self):
        return self.config.dryrun

    def _run(self):
        '''Helper'''
        if not hasattr(self, 'cmdline'):
            self.init_parser()
        if not hasattr(self, 'config'):
            self.parse_args()
        # Determine action or main
        action = getattr(self.config, 'action', None)
        return getattr(self, 'action_%s' % action, 'main')

    def init_logger(self, logger=None, name=None, level=logging.WARN, file=None, handler=None, format='%(asctime)s %(levelname)-7s %(name)s %(message)s'):
        '''Set up logging for this app, should be called before init_parser.
        :param logger: use this logger, all other parameters ignored.
        :param name: create new logger with this name defaults to classname.
        :param level: set logging level.
        :param file: create FileHandler fullpath to logfile.
        :param handler: use this handler.
        :param format: logging format.
        :return: logger instance.
        '''
        if logger is None:
            if name is None:
                name = self.__class__.__name__
            logger = logging.getLogger(name)
            logger.setLevel(level)
            if file:
                handler = logging.FileHandler(file)
            if handler:
                handler.setFormatter(logging.Formatter(format))
                logger.addHandler(handler)
        self.log = logger
        return self.log

    def init_parser(self, dryrun=False, **kwargs):
        '''Add standard commandline options to self.cmdline, a FancyArgumentParser instance .
          - adds any 'action_*' methods to choices of 'action' commandline argument.
          - if self.VERSION found adds --version option
          - if self.log does not exist adds various --log options
        :param dryrun: adds -n/--dryrun option if True
        :param kwargs: passed to FancyArgumentParser
        '''
        self.cmdline = FancyArgumentParser(**kwargs)
        # Determine Action Methods.
        actions = [a[7:] for a in dir(self) if a.startswith('action_')]
        if actions:
            self.actions = self.cmdline.add_subparsers(dest='action', title=argparse.SUPPRESS, metavar='<action>', )
            for action in actions:
                method = getattr(self, 'action_%s' % action)
                foo = self.actions.add_parser(action, help=method.__doc__)
                foo.set_defaults(main=method)
        if hasattr(self, 'VERSION'):
            # We don't add version to kwargs cause argprase defaults to using -v
            # which should be reserved for verbose.
            self.cmdline.add_argument('--version', action='version', version=str(self.VERSION))
        # If logging already configred, don't add as option.
        if not hasattr(self, 'log'):
            self.cmdline.add_log()
        if dryrun:
            self.cmdline.add_argument('-n', '--dryrun', action='store_true', default=False, help='''don't change state''')
        # A convinent facade.
        self.add_argument = self.cmdline.add_argument

    def parse_args(self, args=None, **kwargs):
        '''Parses command line arguments into self.config.
          - Initializes logging.
        :param args: args instead of sys.argv.
        :param kwargs: passed to parse_args()
        :return: (ArgumentParser(), config).
        '''
        if not hasattr(self, 'cmdline'):
            self.init_parser()
        if args is None:
            self.config = self.cmdline.parse_args(**kwargs)
        else:
            self.config = self.cmdline.parse_args(args, **kwargs)
        # Initialize logging early so other code can use it.
        if not hasattr(self, 'log'):
            # Logging to file.
            if self.config.log:
                self.init_logger(level=self.config.log_level, file=self.config.log)
            # Logging to syslog.
            elif self.config.syslog:
                self.init_logger(level=self.config.log_level, handler=logging.handlers.SysLogHandler(facility=self.config.syslog))
            # No logfile or syslog, but a log_level. So, log to stderr.
            elif self.config.log_level:
                self.init_logger(level=self.config.log_level, handler=logging.StreamHandler(sys.stderr), format='%(levelname)-7s %(message)s')

    def parse_config_file(self, fullpath):
        '''Parse file for longoptions.
        This is not "safe", we must trust authors of config_file.
        '''
        if not hasattr(self, 'cmdline'):
            self.init_parser()
        options = dict()
        execfile(fullpath, {}, options)
        self.cmdline.set_defaults(**options)

    def run(self, **kwargs):
        '''Init cmdline (if needed), parse cmdline (if needed), then "run" the app.
        Either run the "action_" or "main" method.
        :param kwargs: passed to to foreground
        '''
        kwargs['main'] = self._run()
        self.foreground(**kwargs)

    def foreground(self, main=None, **kwargs):
        '''Execute in foreground.
        :param main: [self.main] method to execute.
        '''
        if main is None:
            main = getattr(self, 'main')
        exitcode = main()
        sys.exit(exitcode)

    def main(self):
        '''Default main loop of App. Called by daemonize or foreground.
        :return: [0] is used for exit code.
        '''
        return 0


class Daemon(App):
    '''
    self.daemonize() execute in background as daemon.
    self.run() based on cmdline run in foreground or daemonize.

    Signals
      - self.reload() called for SIGHUP.
      - self.cleanup() called for SIGTERM then App exists.
      - self._foo called (if exists) for signal FOO.
    '''

    def init_parser(self, **kwargs):
        super(Daemon, self).init_parser(**kwargs)
        self.cmdline.add_argument('--daemonize', action='store_true', default=False, help='''run as background daemon''')

    def run(self, **kwargs):
        '''Init cmdline (if needed), parse cmdline (if needed), then "run" the app.
        Do one of the following depending on configuration and command line:
          - run "action" (or "main") in foreground
          - run "action" (or "main") in backgroud, daemonize
        :param kwargs: passed to foreground() or daemon.DaemonContext()
        '''
        kwargs['main'] = self._run()
        if getattr(self.config, 'daemonize', None):
            self.daemonize(**kwargs)
        else:
            self.foreground(**kwargs)

    def daemonize(self, pidfile=None, main='main', **kwargs):
        '''Exectue self.main() in background.
        :param main: [self.main] method to execute.
        :param pidfile: full path to pid file.
        :param kwargs: passed to daemon.DaemonContext()
        '''
        # TODO: Need these 3rd party libs.
        import daemon
        import lock
        if pidfile:
            kwargs['pidfile'] = lock.PIDLockfile(pidfile, timeout=0)
        if main is None:
            main = getattr(self, 'main')
        context = daemon.DaemonContext(**kwargs)
        for handler in dir(self):
            name = getattr(signal, handler[1:].upper(), None)  # Remove leading underscore.
            if name is not None:
                context.signal_map[name] = getattr(self, handler)
        if self.log:
            context.files_preserve = [h.stream for h in self.log.handlers]
        with context:
            exitcode = main()
            sys.exit(exitcode)

    def _SIGHUP(self, signal, stackframe):
        self.reload()

    def _SIGTERM(self, signal, stackframe):
        exitcode = self.cleanup()
        sys.exit(exitcode)

    def reload(self):
        '''When daemonized, called for SIGHUP.'''
        pass

    def cleanup(self):
        '''When daemonized, called for SIGTERM, then process exits.
        :return: [0] is used for exit code.
        '''
        return 0


class FancyArgumentParser(argparse.ArgumentParser):
    def add_log(self, parser=None):
        '''Add loging options to parser.
        :param parser: [parser] add arguments to this parser.
        '''
        def loglevel(level):
            '''Python 2.6 needs this.'''
            return getattr(logging, level.upper())
        if parser is None:
            parser = self
        parser.add_argument('--log', metavar='<file>', default=None, help='''log to file''')
        parser.add_argument('--syslog', metavar='<facility>', default=None, help='''log to syslog''')
        parser.add_argument('--log-level', metavar='<level>', default=logging.INFO, type=loglevel, choices=(logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL), help='''set log level''')

    def add_svn(self, parser=None, username='', password='', repo='', repo_metavar='<repo>', repo_dest='svn_repo', repo_help='subversion repository'):
        '''Add svn options to parser.
        :param parser: [parser] add arguments to this parser.
        '''
        if parser is None:
            parser = self
        if repo is not None:
            parser.add_argument('--svn-repo', metavar=repo_metavar, dest=repo_dest, default=repo, help=repo_help)
        if username is not None:
            parser.add_argument('--svn-user', metavar='<user>', dest='svn_username', default=username)
            parser.add_argument('--svn-pass', metavar='<pass>', dest='svn_password', default=password)

    def add_db(self, parser=None, name='', name_help='database', host='', port='', username='', password='', name_metavar='<database>', host_metavar='<host>', host_help=''):
        '''Add database options to parser.
        :param parser: [parser] add arguments to this parser.
        '''
        if parser is None:
            parser = self
        if name is not None:
            parser.add_argument('--db', metavar=name_metavar, default=name, help=name_help)
        if host is not None:
            parser.add_argument('--db-host', metavar=host_metavar, default=host, help=host_help)
        if port is not None:
            parser.add_argument('--db-port', metavar='<port>', default=port)
        if username is not None:
            parser.add_argument('--db-user', metavar='<user>', dest='db_username', default=username)
            parser.add_argument('--db-pass', metavar='<pass>', dest='db_password', default=password)

    def add_aws(self, parser=None):
        '''Add AWS options to parser.
        :param parser: [parser] add arguments to this parser.
        '''
        if parser is None:
            parser = self
        parser.add_argument('--aws-access', metavar='<key>')
        parser.add_argument('--aws-secret', metavar='<key>')
        parser.add_argument('--aws-bucket', metavar='<name>', help='S3 bucket')
        parser.add_argument('--aws-vault', metavar='<name>', help='glacier vault')

    def add_email(self, parser=None, email_from='', email_to=None):
        '''Add email options to parser.
        :param parser: [self] add arguments to this parser.
        :param email_from: [''] default from address.
        :param email_to: [empty] defalt to address or list of addresses.
        '''
        if parser is None:
            parser = self
        if email_to is None:
            email_to = []
        elif isinstance(email_to, str):
            email_to = [email_to, ]
        parser.add_argument('--email-from', metavar='<email>', default=email_from)
        parser.add_argument('--email-to', metavar='<email>', default=email_to, action='append', help='''add to list of notification recipients''')
        parser.add_argument('--email-clear', dest='email_to', action='store_const', const=[], help='''clear list of notification recipients''')
