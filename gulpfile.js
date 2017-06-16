var gulp = require('gulp'),
	config = require('./config.js'),
	del = require('del'),
	plugins = require('gulp-load-plugins')(),
	SPLITER = "-",
	gulpsync = plugins.sync(gulp);

var tasks = [];

var loop = function(object,func){
	for (var key in object){
		var item = object[key]
		func(key,item);
	}
}

var looptasks = function(prefix,cfgs,taskfunc){
	loop(cfgs,function(key,config){
		var type = Object.prototype.toString.call(config);
		if (type != '[object Object]') return
		var name = key?prefix+SPLITER+key:prefix;
		tasks.push(name);
		gulp.task(name,function(){
			return taskfunc(config,key,prefix);
		})
	})
}

var info = function(config,root){
	if (root.info || config.info){
		console.log(config);
	}
}

var global_process = function(config,root){
	info(config,root);
}

var register = function(root){
	loop(root,function(key,item){
		var handler = handlers[key];
		if (handler){
			looptasks(key,item,function(config,key,prefix){
				global_process(config,item);
				return handler(config,key,prefix);
			});
		}

	})
}

var handlers={
	clean:function(config,key,prefix){
		return del(config.src);
	},
	jshint:function(config,key,prefix){
		return gulp.src(config.src)
            .pipe(plugins.jshint())
            .pipe(plugins.jshint.reporter( 'default' ));
	},
	copy:function(config,key,prefix){
		return gulp.src(config.src)
			.pipe(gulp.dest(config.dest));
	},
	concat:function(config,key,prefix){
		return gulp.src(config.src)
			.pipe(plugins.concat(config.name))
			.pipe(gulp.dest(config.dest));

	},
	uglify:function(config,key,prefix){
		return gulp.src(config.src)
			.pipe(plugins.uglify(config.uglifyConf||{}))
			.pipe(plugins.rename({ suffix: config.suffix }))
			.pipe(gulp.dest(config.dest));
	},
	htmlMinify:function(config,key,prefix){
		return gulp.src(config.src)
	        .pipe(plugins.htmlMinify())
	        .pipe(gulp.dest(config.dest))

	},
	minifyCss:function(config,key,prefix){
		return gulp.src(config.src)
		    .pipe(plugins.cleanCss())
		    .pipe(plugins.rename({ suffix: config.suffix }))
		    .pipe(gulp.dest(config.dest));
	},
	rev:function(config,key,prefix){
		return gulp.src(config.src)
			.pipe(plugins.rev())  //set hash key
			.pipe(gulp.dest(config.dest))
			.pipe(plugins.rev.manifest()) //set hash key json
			.pipe(gulp.dest(config.rev)); //dest hash key json
	},
	revCollector:function(config,key,prefix){
			return gulp.src([config.json, config.src])
			.pipe(plugins.revCollector({replaceReved: false,}))
			.pipe(gulp.dest(config.dest));
	},
	doc:function(config,key,prefix){
		var res = plugins.apidoc(config,function(){
		});
		return res
	},
}

register(config);

gulp.task("info",function(){
	console.log(plugins)
	tasks.forEach(function(item){
		console.log('registered task : '+ item)
	})
})
gulp.task('dev', gulpsync.sync([
		'clean',
		'jshint',
		['copy-static','copy-templates'],
		['concat-vendor-css','concat-vendor-js','concat-app-js','concat-app-css'],
		['uglify','uglify-app'],
		['minifyCss','minifyCss-app','htmlMinify'],
		['rev-js','rev-img'],
		['revCollector-css'],
		['rev-css'],
		['revCollector-html'],
		'copy-dist',
		'copy-collect'
		]
	));

gulp.task('default', gulpsync.sync([
		'clean',
		'jshint',
		[/**'doc-api',*/'doc-js'],
		['copy-static','copy-templates'],
		['concat-vendor-css','concat-vendor-js','concat-app-js','concat-app-css'],
		['uglify','uglify-app'],
		['minifyCss','minifyCss-app','htmlMinify'],
		['rev-js','rev-img'],
		['revCollector-css'],
		['rev-css'],
		['revCollector-html'],
		'copy-dist',
		'copy-collect'
		]
	));