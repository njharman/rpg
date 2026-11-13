// MOBS is generated into data.js by ../build-webapp (sw_menagerie.py --minify).

// "12+1", "1/4", "10 (40 hp)" -> a number to sort on.
function leadingNumber(text) {
  var m = /^\s*(\d+)\s*\/\s*(\d+)/.exec(text);
  if (m) {
    return parseInt(m[1], 10) / parseInt(m[2], 10);
  }
  var n = parseFloat(text);
  return isNaN(n) ? 0 : n;
}

var SOURCE_URLS = {
  tohc: 'http://www.talesofthefroggod.com/tome-of-horrors.html'
};

angular.module('Menagerie.service', []).
  factory('gallery', function() {
    // Runs once, so the extra fields are added once however many controllers use it.
    var mobs = MOBS.map(function(mob) {
      mob.ac_dsc = 19 - mob.ac;
      mob.hd_n = leadingNumber(mob.hd);
      mob.cl_n = leadingNumber(mob.cl);
      mob.atk_text = mob.atk.join(', ');
      mob.special_text = (mob.special || []).join(', ');
      mob.source_url = SOURCE_URLS[mob.source] || '';
      return mob;
    });
    return {
      list: function() {
        return mobs;
      }
    };
  });

angular.module('Menagerie', ['Menagerie.service']);

function GalleryCtrl($scope, gallery) {
  $scope.galleryOrder = 'name';
  $scope.gallery = gallery.list();
  $scope.mob = $scope.gallery[0];

  // Takes the mob itself: $index in a filtered, ordered ng-repeat is not an index into the list.
  $scope.select = function(mob) {
    $scope.mob = mob;
  };
}
