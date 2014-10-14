function resetStarrr($el){
	$el.find('i').remove();
	new Starrr($el);

	return false;
}