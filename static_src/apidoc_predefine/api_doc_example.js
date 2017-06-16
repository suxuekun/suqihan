	/**
	* @api {api type} window.apidoc apidoc
	* @apiGroup Functions
	* @apiName API NAME TEXT
	* @apiDescription API desc text
	* @apiVersion 1.0.0
	* 
	* @apiParam {int} a param A desc
	* @apiParam {int} b param B desc 
	* @apiParam {int} c param C desc 
	* @apiSuccessExample Success-Response:
	 {
	   abc:def,
	   others:ext
	 }
	* @apiSuccessExample Empty-Response:
	 {}
	* @apiUse ERROR_USER_NOT_FOUND
	* 
	*/
	function apidoc(a,b,c){
		console.log('apidoc')
		return 'apidoc'
	}