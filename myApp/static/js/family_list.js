// URL が「http://www.example.com?lib=jquery&ver=3」の場合

/**
 * Get the URL parameter value
 *
 */
var myParam = []
myParam=location.href.split('/');

var FCT = {
  paginate_by: 20,
  Choice_Sortkey :[
    'Food_name',
    '-Protein',
    '-FE',
    '-VITA_RAE',
  ],
  Categ_FoodGrp: [
  'Cereals and their products',
  'Roots, tubers and their products',
  'Legumes and their products',
  'Vegetables and their products',
  'Fruits and their products',
  'Nuts, Seeds and their products',
  'Meat, poultry and their products',
  'Eggs and their products',
  'Fish and their products',
  'Milk and their products',
  'Bevarages and their products',
  'Miscellaneous',
  ]
};
