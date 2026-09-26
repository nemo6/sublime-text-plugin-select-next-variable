;( async () => {

	console.log( "test" )

	// detect current meta block ( meta.block.js ) before searching match for variable name

	{

	let yolo = null
	let volt = 15

	foo ( volt * 2 , yolo ) // v
	let bar = null
	function foo ( xv , yv ){
		console.log( x )
	}

	}

	{

		let yolo = null
		let volt = 15

		foo ( volt * 2 , yolo ) // v
		let bar = null
		function foo ( xv , yv ){
			console.log( x )
		}

	}
})()
