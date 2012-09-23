function navSelect(obj,nav)
{
  var selectPos = obj.className.search('-selected');
  var className = obj.className;
  
  if (selectPos == -1) {
	var navObjs = document.getElementsByClassName(nav);
	for (i=0; i<navObjs.length; i++) {
	  if (navObjs[i].children[0].children[0].className.search('-selected') != -1) {
	  	navObjs[i].children[0].children[0].className = className;
	  }
	}
	obj.className = className + '-selected'
  } else {
  	obj.className = className.substring(0,selectPos);
  }
}


function showChange()
{
  var divSave = document.getElementsByClassName('admin-action');

  divSave[0].style.display = 'block';
  divSave[0].innerHTML = 'Changes saved';
}