var path = require('path');
	_path = _P = path.join,
	_suffix = _S = (x) =>{
		return "." + x;
	},
	_folder = _F = (x) =>{
		return "/" + x;
	};
var STATIC = "static",
	TEMPLATES= "templates",
	CONFIG = "config",
	MIN = "min",
	REP = "rep",
	REV = "rev",
	SRC = "src",
	BUILD = "build",
	DEV = "dev",
	DIST = "dist",
	APIDOC = "apidoc",
	API = "api",
	DOC = "doc",
	JS = "js",
	JSON = "json",
	HTML = "html",
	CSS = "css",
	IMG = "images",
	APP = "app",
	VENDOR = "vendor",
	ALL = "**/*",
	ALL_JS = ALL+_S(JS),
	ALL_CSS = ALL+_S(CSS),
	ALL_HTML = ALL+_S(HTML),
	ALL_JSON = ALL+_S(JSON),
	ROOT = "./";

var app = "suqihan";

var src = _P(ROOT,app),
	src_static = _P(ROOT,"static_src"),
	src_template = _P(ROOT,"templates_src"),
	dest = _P(ROOT,DIST),
	build = _P(ROOT,BUILD),
	build_src = _P(build,SRC),
	build_src_static = _P(build_src,STATIC);
	build_src_template = _P(build_src,TEMPLATES)
	build_min = _P(build,MIN),
	build_min_static = _P(build_min,STATIC);
	build_rep = _P(build,REP),
	build_rep_static = _P(build_rep,STATIC);
	build_rev = _P(build,REV),
	build_rev_static = _P(build_rev,STATIC);
	build_json = _P(build,JSON),
	doc = _P(ROOT,DOC),
	apidoc = _P(doc,API),
	jsdoc = _P(doc,JS);

var exp = {
	_P:_P,
	_S:_S,
	_F:_F,
	_path:_path,
	_suffix:_suffix,
	_folder:_folder,
	clean:{
        "":{
        	src: [_P(dest,ALL),_P(build,ALL),_P(doc,ALL)],
        }
    },
	jshint:{
		"":{
			src: [
				_P(src_static,SRC,ALL_JS),
				_P(src_static,APP,ALL_JS),
			]
		}
	},
	doc:{
		api:{
			src:src,
			dest:apidoc,
			config:_P(ROOT,CONFIG,API),
		},
		js:{
			src:src_static,
			dest: jsdoc,
			config:_path(ROOT,CONFIG,JS),
		}
	},
	copy:{
		static:{
			src:_P(src_static,ALL),
			dest:_P(build_src_static)
		},
		templates:{
			src:_P(src_template,ALL),
			dest:_P(build_src_template)
		},
		dist:{
			src:_P(build_rev,ALL),
			dest:dest
		},
		collect:{
			src:_P(dest,ALL),
			dest:src,
		}
	},
	concat:{// concat
		info:true,
		'vendor-css':{
			src:[
				_P(build_src_static,VENDOR,ALL_CSS)
			],
			dest:_P(build_src_static,CSS),
			name:'vendor.css',
		},
		'vendor-js':{
			src:[
				_P(build_src_static,VENDOR,ALL_JS),
			],
			dest:_P(build_src_static,JS),
			name:'vendor.js',
		},

		'app-css':{
			src:_P(build_src_static,SRC,ALL_CSS),
			dest:_P(build_src_static,CSS),
			name:'app.css',
		},
		'app-js':{
			src:_P(build_src_static,SRC,ALL_JS),
			dest:_P(build_src_static,JS),
			name:'app.js',
		}
	},
	uglify:{
		info:true,
		"":{
			src:_P(build_src_static,JS,ALL_JS),
			dest:_P(build_min_static,JS),
			uglifyConf: {
				mangle:false,
			},
		},
		app:{
			src:_P(build_src_static,APP,ALL_JS),
			dest:_P(build_min_static,APP),
			uglifyConf: {
				mangle:false,
			},
		}

	},
	minifyCss:{
		info:true,
		"":{
			src:_P(build_src_static,CSS,ALL_CSS),
			dest:_P(build_min_static,CSS),
		},
		app:{
			src:_P(build_src_static,APP,ALL_CSS),
			dest:_P(build_min_static,APP),
		}
	},
	htmlMinify:{
		"":{
			src:_P(build_src,ALL_HTML),
			dest:_P(build_min),
		}
	},
	rev:{
		img:{
			src:_P(build_src_static,APP,IMG,ALL),
			dest:_P(build_rev_static,APP,IMG),
			rev:_P(build_json,IMG),
		},
		js:{
			src:_P(build_min_static,ALL_JS),
			dest:_P(build_rev_static),
			rev:_P(build_json,JS),
		},
		css:{
			src:_P(build_rep_static,ALL_CSS),
			dest:_P(build_rev_static),
			rev:_P(build_json,CSS),
		}
	},
	revCollector:{
		css:{
			json: _P(build_json,ALL+_S(JSON)),
        	src: _P(build_min_static,ALL+_S(CSS)),
        	dest: _P(build_rep_static),
		},
		html:{
			json: _P(build_json,ALL+_S(JSON)),
        	src: _P(build_min,ALL+_S(HTML)),
        	dest: _P(build_rev),
		}

	}
}

module.exports = exp