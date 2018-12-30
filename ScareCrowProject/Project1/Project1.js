
var canvas;
var gl;
var program;

var nFaces;
var sphere_faces;

var axis = 0;
var xAxis = 0;
var yAxis = 1;
var zAxis = 2;
var theta = [90, 0, 0];

var theta2 = [90,0,0];
var theta3 = [90,0,0];
var theta4 = [90,0,0];

var points = [];
var indices = [];
var UVs= [];
var normals = [];
var buffers = [];

var points2 = [];
var normals2 = [];
var UVs2 = [];
var indices2 = [];
var buffers2 = [];

var points3 = [];
var normals3 = [];
var UVs3 = [];
var indices3 = [];
var buffers3 = [];

var points4 = [];
var normals4 = [];
var UVs4 = [];
var indices4 = [];
var buffers4 = [];

var points5 = [];
var normals5 = [];
var UVs5 = [];
var indices5 = [];
var buffers5 = [];

var points6 = [];
var normals6 = [];
var UVs6 = [];
var indices6 = [];
var buffers6 = [];

var points7 = [];
var normals7 = [];
var UVs7 = [];
var indices7 = [];
var buffers7 = [];

var points8 = [];
var normals8 = [];
var UVs8 = [];
var indices8 = [];
var buffers8 = [];

var displacement_y = 1.;
var velocity_y = 0.;
var axis_speed = 2.;
var disp_val = .03;
var vel_dec = .1;

var timer = 1.5;
var timer2 = 0;
var head_timer = 0;
var animation_check = false;

var temp_timer = 1.5;
var temp_timer2 = 0;

var temp_velocity = 0;

var pause_flag = false;

window.onload = function init()
{
    initGL();

	//First Cylinder
    cylinder_post1();
	
	cylinder_post2();
	
	cylinder_body();
	
	cylinder_right_arm();
	
	cylinder_left_arm();
	
	cylinder_left_leg();
	
	cylinder_right_leg();
	
	sphere_head();
	
	initTexture();
	
	initTexture2();
	
	document.getElementById("Start Animation").onclick = function () {
		animation_check = true;
		timer = temp_timer;
		timer2 = temp_timer2;
	};
	
	document.getElementById("Pause Animation").onclick = function () {
		animation_check = false;
		timer = 0;
		timer2 = 0;
		head_timer = 0;
	};
	
	render();
}
var squareTexture;

//BOILERPLATE functions used for initializing textures
function initTexture() {
    squareTexture = gl.createTexture();
    var squareImage = new Image();
    squareImage.onload = function () { handleTextureLoaded(squareImage, squareTexture); }
    squareImage.src = "Material/HelloWorld.png";
}
//BOILERPLATE continued
function handleTextureLoaded(image, texture) {
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.bindTexture(gl.TEXTURE_2D, null);
}


var squareTexture2;

//BOILERPLATE functions used for initializing textures
function initTexture2() {
    squareTexture2 = gl.createTexture();
    var squareImage2 = new Image();
    squareImage2.onload = function () { handleTextureLoaded2(squareImage2, squareTexture2); }
    squareImage2.src = "Material/marble10.png";
}
//BOILERPLATE continued
function handleTextureLoaded2(image, texture2) {
    gl.bindTexture(gl.TEXTURE_2D, texture2);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_NEAREST);
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.bindTexture(gl.TEXTURE_2D, null);
}

function initGL()
{
    canvas = document.getElementById("gl-canvas");

    gl = WebGLUtils.setupWebGL(canvas);
    if (!gl) { alert("WebGL isn't available"); }

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(1.0, 1.0, 1.0, 1.0);

    program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);
	
}

//Definitely put rotation in here!
//Rotation has been added. Specify angle and rotation type to rotate points
//rot_type stands for the type of rotation to be performed: "xy" (x-y axis rotation)
//															"xz" (x-z axis rotation)
//															"yz" (y-z axis rotation)
//															"none" (no axis rotation)
function create_cylinder_points(radius_cyl,z_off, x_axis, y_axis, z_axis, point_buf, normal_buf, uv_buf, indice_buf, angle, rot_type)
{
	
	radius = radius_cyl;
	z_offset = z_off;
	PI = Math.PI
	
	
	if(rot_type == "none")
	{
		center_point = vec3((0+x_axis),(0+y_axis),0+z_axis);
		//First point!
		point_buf.push(center_point);
		normal_buf.push(center_point);
	}
	
	if(rot_type == "xy")
	{
		center_point = vec3((0+x_axis)*Math.cos(angle)-(0+y_axis)*Math.sin(angle),(0+y_axis)*Math.cos(angle)+(0+x_axis)*Math.sin(angle),0+z_axis);
		//First point!
		point_buf.push(center_point);
		normal_buf.push(center_point);
	}
	
	if(rot_type == "xz")
	{
		center_point = vec3((0+x_axis)*Math.cos(angle)-(0+z_axis)*Math.sin(angle),(0+y_axis),(0+z_axis)*Math.cos(angle)+(0+x_axis)*Math.sin(angle));
		//First point!
		point_buf.push(center_point);
		normal_buf.push(center_point);
	}
	
	if(rot_type == "yz")
	{
		center_point = vec3((0+x_axis),(0+y_axis)*Math.cos(angle)-(0+z_axis)*Math.sin(angle),(0+z_axis)*Math.cos(angle)+(0+y_axis)*Math.sin(angle));
		//First point!
		point_buf.push(center_point);
		normal_buf.push(center_point);
	}
	
	
	for(z = 0; z < 2; z++)
	{
		for(i = 0; i < 361; i++)
		{
			if(rot_type == "none")
			{
				point_buf.push(vec3(((radius*Math.cos(2*PI*i/360))+x_axis),((radius*Math.sin(2*PI*i/360))+y_axis),(z*z_offset)+z_axis));
				normal_buf.push(((radius*Math.cos(2*PI*i/360))+x_axis),((radius*Math.sin(2*PI*i/360))+y_axis),(z*z_offset)+z_axis);
				//UVs.push(i*Math.PI,i);	
			}
			if(rot_type == "xy")
			{
				point_buf.push(vec3(((radius*Math.cos(2*PI*i/360))+x_axis)*Math.cos(angle)-((radius*Math.sin(2*PI*i/360))+y_axis)*Math.sin(angle),((radius*Math.sin(2*PI*i/360))+y_axis)*Math.cos(angle)+((radius*Math.cos(2*PI*i/360))+x_axis)*Math.sin(angle),(z*z_offset)+z_axis));
				normal_buf.push(((radius*Math.cos(2*PI*i/360))+x_axis)*Math.cos(angle)-((radius*Math.sin(2*PI*i/360))+y_axis)*Math.sin(angle),((radius*Math.sin(2*PI*i/360))+y_axis)*Math.cos(angle)+((radius*Math.cos(2*PI*i/360))+x_axis)*Math.sin(angle),(z*z_offset)+z_axis);
				//UVs.push(i*Math.PI,i);
			}
			if(rot_type == "xz")
			{
				point_buf.push(vec3(((radius*Math.cos(2*PI*i/360))+x_axis)*Math.cos(angle)-((z*z_offset)+z_axis)*Math.sin(angle),((radius*Math.sin(2*PI*i/360))+y_axis),((z*z_offset)+z_axis)*Math.cos(angle)+((radius*Math.cos(2*PI*i/360))+x_axis)*Math.sin(angle)));
				normal_buf.push(((radius*Math.cos(2*PI*i/360))+x_axis)*Math.cos(angle)-((z*z_offset)+z_axis)*Math.sin(angle),((radius*Math.sin(2*PI*i/360))+y_axis),((z*z_offset)+z_axis)*Math.cos(angle)+((radius*Math.cos(2*PI*i/360))+x_axis)*Math.sin(angle));
				//UVs.push(i*Math.PI,i);
			}
			
			if(rot_type == "yz")
			{
				point_buf.push(vec3(((radius*Math.cos(2*PI*i/360))+x_axis),((radius*Math.sin(2*PI*i/360))+y_axis)*Math.cos(angle)-((z*z_offset)+z_axis)*Math.sin(angle),((z*z_offset)+z_axis)*Math.cos(angle)+((radius*Math.sin(2*PI*i/360))+y_axis)*Math.sin(angle)));
				normal_buf.push(((radius*Math.cos(2*PI*i/360))+x_axis),((radius*Math.sin(2*PI*i/360))+y_axis)*Math.cos(angle)-((z*z_offset)+z_axis)*Math.sin(angle),((z*z_offset)+z_axis)*Math.cos(angle)+((radius*Math.sin(2*PI*i/360))+y_axis)*Math.sin(angle));
				//UVs.push(i*Math.PI,i);
			}
		}
	}
	
	
	if(rot_type == "none")
	{
		offset_z = vec3((0+x_axis),(0+y_axis),z_offset+z_axis);
		point_buf.push(offset_z);
		normal_buf.push(offset_z);
	}
	
	if(rot_type == "xy")
	{
		offset_z = vec3((0+x_axis)*Math.cos(angle)-(0+y_axis)*Math.sin(angle),(0+y_axis)*Math.cos(angle)+(0+x_axis)*Math.sin(angle),z_offset+z_axis);
		point_buf.push(offset_z);
		normal_buf.push(offset_z);
	}
	
	if(rot_type == "xz")
	{
		offset_z = vec3((0+x_axis)*Math.cos(angle)-(z_offset+z_axis)*Math.sin(angle),(0+y_axis),(z_offset+z_axis)*Math.cos(angle)+(0+x_axis)*Math.sin(angle));
		point_buf.push(offset_z);
		normal_buf.push(offset_z);
	}
	
	if(rot_type == "yz")
	{
		offset_z = vec3((0+x_axis),(0+y_axis)*Math.cos(angle)-(z_offset+z_axis)*Math.sin(angle),(z_offset+z_axis)*Math.cos(angle)+(0+y_axis)*Math.sin(angle));
		point_buf.push(offset_z);
		normal_buf.push(offset_z);
	}
	
	uv_buf.push(
		vec2(0.,0.),
		vec2(1.,0.),
		vec2(1.,1.),
		vec2(0.,1.),
		vec2(1.,1.),
		vec2(0.,1.),
		vec2(0.,0.),
		vec2(1.,0.)
    );
	
	
	for(i = 1; i < 361; i++)
	{
		indice_buf.push(0,i,i+1);
	}
	
	
	for(i = 361; i < (361*2); i++)
	{
		indice_buf.push(722, i, i+1);
	}
	
	for(i = 0; i < 361; i++)
	{
		indice_buf.push(i, i+1, i+361);
		indice_buf.push(i+361, (i+1)+361, i+1);
	}
	

    nFaces = indice_buf.length;
}

function create_sphere_points(radius_sphere, x_axis, y_axis, z_axis, point_buf, normal_buf, uv_buf, indice_buf)
{
	
	radius = radius_sphere;
	z_offset = .13;
	PI = Math.PI;

	
	center_point = vec3((0+x_axis),(0+y_axis),0+z_axis);
	//First point!
	point_buf.push(center_point);
	normal_buf.push(center_point);
	
	//uv_buf.push(vec2(0,0));	
	
	
	for(z = 0; z < 6; z++)
	{	
		if(z<(6/2))
		{
			radius += .06;
		}
		if(z>(6/2))
		{
			radius -= .06;
		}
		for(i = 0; i < 361; i++)
		{
			point_buf.push(vec3(((radius*Math.cos(2*PI*i/360))+x_axis),((radius*Math.sin(2*PI*i/360))+y_axis),(z*z_offset)+z_axis));
			normal_buf.push(((radius*Math.cos(2*PI*i/360))+x_axis),((radius*Math.sin(2*PI*i/360))+y_axis),(z*z_offset)+z_axis);
			uv_buf.push(vec2((i/360)*(z+1),i/360));	
		}
	}
	
	
	for(j = 1; j < 6; j++)
	{
		offset_z = vec3((0+x_axis),(0+y_axis),(j*z_offset)+z_axis);
		point_buf.push(offset_z);
		normal_buf.push(offset_z);
	}
	
	/*
	uv_buf.push(
		vec2(0.,0.),
		vec2(1.,0.),
		vec2(1.,1.),
		vec2(0.,1.),
		vec2(1.,1.),
		vec2(0.,1.),
		vec2(0.,0.),
		vec2(1.,0.)
    );
	*/
	
	for(z = 1; z < 7; z++)
	{
		if(z == 1)
		{
			for(i = 0; i < 361; i++)
			{
				indice_buf.push(0,i,i+1);
			}
		}
		
		else
		{
			for(i = (361*(z-1))+1; i < (361*z); i++)
			{
				indice_buf.push(2167+(z-2), i, i+1);
			}
		}
	}
	
	for(j = 0; j < 5; j++)
	{
		for(i = 0; i < 361; i++)
		{
			indice_buf.push(i+(361*j), i+(361*j)+1, i+(361*j)+361);
			indice_buf.push(i+(361*j)+361, (i+(361*j)+1)+361, i+(361*j)+1);
		}
	}
	
	
	sphere_faces = indice_buf.length;
}

function cylinder_post1()
{
	create_cylinder_points(.1,3,0,0,0,points,normals,UVs,indices,(0), "none");
	
    //Link data to vertex shader input
    var vPosition = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);


    //Link data to vertex shader input
    var vUV = gl.getAttribLocation(program, "vUV");
    gl.vertexAttribPointer(vUV, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV);
	
	//Create buffer to store the vertex coordinates
    var vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(points), gl.STATIC_DRAW);
    buffers.push(vBuffer);

    //Create buffer to store the normals
    var nBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(normals), gl.STATIC_DRAW);
    buffers.push(nBuffer);
	
    //Create buffer to store the texture coordinates
    var tcBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tcBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(UVs), gl.STATIC_DRAW);
    buffers.push(tcBuffer);

    //Create buffer to store the triangle elements
    var tBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, tBuffer);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(indices)), gl.STATIC_DRAW);
    buffers.push(tBuffer);

    //Link data to vertex shader input
    var vNormal = gl.getAttribLocation(program, "vNormal");
    gl.vertexAttribPointer(vNormal, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal);
}

function cylinder_post2()
{
	create_cylinder_points(.1,3,1,0,-1.5,points2,normals2,UVs2,indices2,(Math.PI/2), "xz");
	
	
	//Link data to vertex shader input
    var vPosition2 = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition2, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition2);


    //Link data to vertex shader input
    var vUV2 = gl.getAttribLocation(program, "vUV");
    gl.vertexAttribPointer(vUV2, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV2);
	
	//Create buffer to store the vertex coordinates
    var vBuffer2 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer2);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(points2), gl.STATIC_DRAW);
    buffers2.push(vBuffer2);

    //Create buffer to store the normals
    var nBuffer2 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer2);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(normals2), gl.STATIC_DRAW);
    buffers2.push(nBuffer2);
	
    //Create buffer to store the texture coordinates
    var tcBuffer2 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tcBuffer2);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(UVs2), gl.STATIC_DRAW);
    buffers2.push(tcBuffer2);

    //Create buffer to store the triangle elements
    var tBuffer2 = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, tBuffer2);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(indices2)), gl.STATIC_DRAW);
    buffers2.push(tBuffer2);

    //Link data to vertex shader input
    var vNormal2 = gl.getAttribLocation(program, "vNormal");
    gl.vertexAttribPointer(vNormal2, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal2);
	
}

function cylinder_body()
{
	
	create_cylinder_points(.25,1.2,0,.3,.8,points3,normals3,UVs3,indices3,(0), "none");
	
    //Link data to vertex shader input
    var vPosition3 = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition3, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition3);


    //Link data to vertex shader input
    var vUV3 = gl.getAttribLocation(program, "vUV");
    gl.vertexAttribPointer(vUV3, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV3);
	
	//Create buffer to store the vertex coordinates
    var vBuffer3 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer3);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(points3), gl.STATIC_DRAW);
    buffers3.push(vBuffer3);

    //Create buffer to store the normals
    var nBuffer3 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer3);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(normals3), gl.STATIC_DRAW);
    buffers3.push(nBuffer3);
	
    //Create buffer to store the texture coordinates
    var tcBuffer3 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tcBuffer3);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(UVs3), gl.STATIC_DRAW);
    buffers3.push(tcBuffer3);

    //Create buffer to store the triangle elements
    var tBuffer3 = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, tBuffer3);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(indices3)), gl.STATIC_DRAW);
    buffers3.push(tBuffer3);

    //Link data to vertex shader input
    var vNormal3 = gl.getAttribLocation(program, "vNormal");
    gl.vertexAttribPointer(vNormal3, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal3);
	
}


function cylinder_right_arm()
{
	create_cylinder_points(.075,1,0,0,0,points4,normals4,UVs4,indices4,(Math.PI/2), "xz");
	
    //Link data to vertex shader input
    var vPosition4 = gl.getAttribLocation(program, "vPosition4");
    gl.vertexAttribPointer(vPosition4, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition4);


    //Link data to vertex shader input
    var vUV4 = gl.getAttribLocation(program, "vUV4");
    gl.vertexAttribPointer(vUV4, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV4);
	
	//Create buffer to store the vertex coordinates
    var vBuffer4 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer4);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(points4), gl.STATIC_DRAW);
    buffers4.push(vBuffer4);

    //Create buffer to store the normals
    var nBuffer4 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer4);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(normals4), gl.STATIC_DRAW);
    buffers4.push(nBuffer4);
	
    //Create buffer to store the texture coordinates
    var tcBuffer4 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tcBuffer4);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(UVs4), gl.STATIC_DRAW);
    buffers4.push(tcBuffer4);

    //Create buffer to store the triangle elements
    var tBuffer4 = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, tBuffer4);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(indices4)), gl.STATIC_DRAW);
    buffers4.push(tBuffer4);

    //Link data to vertex shader input
    var vNormal4 = gl.getAttribLocation(program, "vNormal4");
    gl.vertexAttribPointer(vNormal4, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal4);
}


function cylinder_left_arm()
{
	create_cylinder_points(.075,1,0,0,0,points5,normals5,UVs5,indices5,(Math.PI/2), "xz");
	
    //Link data to vertex shader input
    var vPosition5 = gl.getAttribLocation(program, "vPosition3");
    gl.vertexAttribPointer(vPosition5, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition5);


    //Link data to vertex shader input
    var vUV5 = gl.getAttribLocation(program, "vUV3");
    gl.vertexAttribPointer(vUV5, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV5);
	
	//Create buffer to store the vertex coordinates
    var vBuffer5 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer5);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(points5), gl.STATIC_DRAW);
    buffers5.push(vBuffer5);

    //Create buffer to store the normals
    var nBuffer5 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer5);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(normals5), gl.STATIC_DRAW);
    buffers5.push(nBuffer5);
	
    //Create buffer to store the texture coordinates
    var tcBuffer5 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tcBuffer5);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(UVs5), gl.STATIC_DRAW);
    buffers5.push(tcBuffer5);

    //Create buffer to store the triangle elements
    var tBuffer5 = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, tBuffer5);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(indices5)), gl.STATIC_DRAW);
    buffers5.push(tBuffer5);

    //Link data to vertex shader input
    var vNormal5 = gl.getAttribLocation(program, "vNormal3");
    gl.vertexAttribPointer(vNormal5, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal5);
}



function cylinder_left_leg()
{
	create_cylinder_points(.075,1,.15,.2,1.7,points6,normals6,UVs6,indices6,(0), "none");
	
    //Link data to vertex shader input
    var vPosition6 = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition6, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition6);


    //Link data to vertex shader input
    var vUV6 = gl.getAttribLocation(program, "vUV");
    gl.vertexAttribPointer(vUV6, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV6);
	
	//Create buffer to store the vertex coordinates
    var vBuffer6 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer6);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(points6), gl.STATIC_DRAW);
    buffers6.push(vBuffer6);

    //Create buffer to store the normals
    var nBuffer6 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer6);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(normals6), gl.STATIC_DRAW);
    buffers6.push(nBuffer6);
	
    //Create buffer to store the texture coordinates
    var tcBuffer6 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tcBuffer6);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(UVs6), gl.STATIC_DRAW);
    buffers6.push(tcBuffer6);

    //Create buffer to store the triangle elements
    var tBuffer6 = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, tBuffer6);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(indices6)), gl.STATIC_DRAW);
    buffers6.push(tBuffer6);

    //Link data to vertex shader input
    var vNormal6 = gl.getAttribLocation(program, "vNormal");
    gl.vertexAttribPointer(vNormal6, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal6);
}



function cylinder_right_leg()
{
	create_cylinder_points(.075,1,-.15,.2,1.7,points7,normals7,UVs7,indices7,(0), "none");
	
    //Link data to vertex shader input
    var vPosition7 = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition7, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition7);


    //Link data to vertex shader input
    var vUV7 = gl.getAttribLocation(program, "vUV");
    gl.vertexAttribPointer(vUV7, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV7);
	
	//Create buffer to store the vertex coordinates
    var vBuffer7 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer7);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(points7), gl.STATIC_DRAW);
    buffers7.push(vBuffer7);

    //Create buffer to store the normals
    var nBuffer7 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer7);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(normals7), gl.STATIC_DRAW);
    buffers7.push(nBuffer7);
	
    //Create buffer to store the texture coordinates
    var tcBuffer7 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tcBuffer7);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(UVs7), gl.STATIC_DRAW);
    buffers7.push(tcBuffer7);

    //Create buffer to store the triangle elements
    var tBuffer7 = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, tBuffer7);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(indices7)), gl.STATIC_DRAW);
    buffers7.push(tBuffer7);

    //Link data to vertex shader input
    var vNormal7 = gl.getAttribLocation(program, "vNormal");
    gl.vertexAttribPointer(vNormal7, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal7);
}


function sphere_head()
{
	create_sphere_points(.05,0,0,0,points8,normals8,UVs8,indices8);

    //Link data to vertex shader input
    var vPosition8 = gl.getAttribLocation(program, "vPosition2");
    gl.vertexAttribPointer(vPosition8, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition8);


    //Link data to vertex shader input
    var vUV8 = gl.getAttribLocation(program, "vUV2");
    gl.vertexAttribPointer(vUV8, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV8);
	
	//Create buffer to store the vertex coordinates
    var vBuffer8 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer8);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(points8), gl.STATIC_DRAW);
    buffers8.push(vBuffer8);

    //Create buffer to store the normals
    var nBuffer8 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, nBuffer8);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(normals8), gl.STATIC_DRAW);
    buffers8.push(nBuffer8);
	
    //Create buffer to store the texture coordinates
    var tcBuffer8 = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, tcBuffer8);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(UVs8), gl.STATIC_DRAW);
    buffers8.push(tcBuffer8);

    //Create buffer to store the triangle elements
    var tBuffer8 = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, tBuffer8);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(flatten(indices8)), gl.STATIC_DRAW);
    buffers8.push(tBuffer8);

    //Link data to vertex shader input
    var vNormal8 = gl.getAttribLocation(program, "vNormal2");
    gl.vertexAttribPointer(vNormal8, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal8);
}


function render()
{
	
    gl.enable(gl.DEPTH_TEST);
    gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
	
	//First Post
	Draw_Cylinder_Component(buffers);
	//Second (Cross) Post
	Draw_Cylinder_Component(buffers2);
	//Body Cylinder
	Draw_Cylinder_Component(buffers3);
	//Left Arm Cylinder
	Draw_Cylinder_Component_LArm(buffers4);
	//Draw_Cylinder_Component(buffers4);
	//Right Arm Cylinder
	Draw_Cylinder_Component_RArm(buffers5);
	//Draw_Cylinder_Component(buffers5);
	//Left Leg Cylinder
	Draw_Cylinder_Component(buffers6);
	//Right Leg Cylinder
	Draw_Cylinder_Component(buffers7);
	//Spherical Head
	Draw_Sphere_Component(buffers8);
	
	requestAnimationFrame(render);
}

function Draw_Cylinder_Component(buf)
{
	theta[0] = 105;
	theta[1] = -15;
	
	//This changes rotation of object
    gl.uniform3fv(gl.getUniformLocation(program, "theta"), theta);
	
	//Texture binding
	gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, squareTexture);
    gl.uniform1i(gl.getUniformLocation(program, "uSampler"), 0);

    //Link data to vertex shader input
    var vPosition = gl.getAttribLocation(program, "vPosition");
    var vNormal = gl.getAttribLocation(program, "vNormal");
    var vUV = gl.getAttribLocation(program, "vUV");

	//Cylinder Body drawing
	gl.uniform1i(gl.getUniformLocation(program, "useTexture"), false);
	gl.uniform1i(gl.getUniformLocation(program, "useTexture2"), false);
	
	gl.uniform1i(gl.getUniformLocation(program, "obj1"), true);
	gl.uniform1i(gl.getUniformLocation(program, "obj2"), false);
	gl.uniform1i(gl.getUniformLocation(program, "obj3"), false);
	gl.uniform1i(gl.getUniformLocation(program, "obj4"), false);
	
    gl.drawElements(gl.TRIANGLES, nFaces, gl.UNSIGNED_SHORT, 0);
	
	//Draw Cylinder Body
    gl.bindBuffer(gl.ARRAY_BUFFER, buf[0]);
    gl.vertexAttribPointer(vPosition, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);

    gl.bindBuffer(gl.ARRAY_BUFFER, buf[1]);
    gl.vertexAttribPointer(vNormal, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal);

    gl.bindBuffer(gl.ARRAY_BUFFER, buf[2]);
    gl.vertexAttribPointer(vUV, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buf[3]);
	
    gl.drawElements(gl.TRIANGLES, nFaces, gl.UNSIGNED_SHORT, 0);
}

function Draw_Sphere_Component(buf)
{	
	
	theta2[1] += head_timer;
	
	if(animation_check == true)
	{
		head_timer = 5;
	}
	
	//This changes rotation of object
    gl.uniform3fv(gl.getUniformLocation(program, "theta2"), theta2);

	//Texture binding
	gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, squareTexture);
    gl.uniform1i(gl.getUniformLocation(program, "uSampler"), 0);

    //Link data to vertex shader input
    var vPosition = gl.getAttribLocation(program, "vPosition2");
    var vNormal = gl.getAttribLocation(program, "vNormal2");
    var vUV = gl.getAttribLocation(program, "vUV2");

	//Sphere Body drawing
	gl.uniform1i(gl.getUniformLocation(program, "useTexture"), false);
	gl.uniform1i(gl.getUniformLocation(program, "useTexture2"), false);
	
	gl.uniform1i(gl.getUniformLocation(program, "obj1"), false);
	gl.uniform1i(gl.getUniformLocation(program, "obj2"), true);
	gl.uniform1i(gl.getUniformLocation(program, "obj3"), false);
	gl.uniform1i(gl.getUniformLocation(program, "obj4"), false);
	
	
    gl.drawElements(gl.TRIANGLES, sphere_faces, gl.UNSIGNED_SHORT, 0);
	
	//Draw Sphere Body
    gl.bindBuffer(gl.ARRAY_BUFFER, buf[0]);
    gl.vertexAttribPointer(vPosition, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);

    gl.bindBuffer(gl.ARRAY_BUFFER, buf[1]);
    gl.vertexAttribPointer(vNormal, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal);

    gl.bindBuffer(gl.ARRAY_BUFFER, buf[2]);
    gl.vertexAttribPointer(vUV, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buf[3]);
	
    gl.drawElements(gl.TRIANGLES, sphere_faces, gl.UNSIGNED_SHORT, 0);
}


function Draw_Cylinder_Component_LArm(buf)
{
	
	if(animation_check == true)
	{
		theta3[2] += timer;
		
		timer = timer + .1;
		
		if(timer >= 2.5)
		{
			timer = -2.4;
		}
		
		temp_timer = timer;
	}

	
	//This changes rotation of object
    gl.uniform3fv(gl.getUniformLocation(program, "theta3"), theta3);
	
	//Texture binding
	gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, squareTexture);
    gl.uniform1i(gl.getUniformLocation(program, "uSampler"), 0);

    //Link data to vertex shader input
    var vPosition = gl.getAttribLocation(program, "vPosition3");
    var vNormal = gl.getAttribLocation(program, "vNormal3");
    var vUV = gl.getAttribLocation(program, "vUV3");

	//Cylinder Body drawing
	gl.uniform1i(gl.getUniformLocation(program, "useTexture"), false);
	gl.uniform1i(gl.getUniformLocation(program, "useTexture2"), false);
	
	gl.uniform1i(gl.getUniformLocation(program, "obj1"), false);
	gl.uniform1i(gl.getUniformLocation(program, "obj2"), false);
	gl.uniform1i(gl.getUniformLocation(program, "obj3"), true);
	gl.uniform1i(gl.getUniformLocation(program, "obj4"), false);
	
    gl.drawElements(gl.TRIANGLES, nFaces, gl.UNSIGNED_SHORT, 0);
	
	//Draw Cylinder Body
    gl.bindBuffer(gl.ARRAY_BUFFER, buf[0]);
    gl.vertexAttribPointer(vPosition, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);

    gl.bindBuffer(gl.ARRAY_BUFFER, buf[1]);
    gl.vertexAttribPointer(vNormal, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal);

    gl.bindBuffer(gl.ARRAY_BUFFER, buf[2]);
    gl.vertexAttribPointer(vUV, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buf[3]);
	
    gl.drawElements(gl.TRIANGLES, nFaces, gl.UNSIGNED_SHORT, 0);
}


function Draw_Cylinder_Component_RArm(buf)
{
	theta4[0] = 105;
	theta4[2] += timer2;
	
	
	if(animation_check == true)
	{
		timer2 = timer2 + .1;
		
		if(timer2 >= 2.5)
		{
			timer2 = -2.4;
		}
		
		temp_timer2 = timer2;
	}
	
	//theta[1] += .1;
	//This changes rotation of object
    gl.uniform3fv(gl.getUniformLocation(program, "theta4"), theta4);
	
	
	//Texture binding
	gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, squareTexture);
    gl.uniform1i(gl.getUniformLocation(program, "uSampler"), 0);

    //Link data to vertex shader input
    var vPosition = gl.getAttribLocation(program, "vPosition4");
    var vNormal = gl.getAttribLocation(program, "vNormal4");
    var vUV = gl.getAttribLocation(program, "vUV4");

	//Cylinder Body drawing
	gl.uniform1i(gl.getUniformLocation(program, "useTexture"), false);
	gl.uniform1i(gl.getUniformLocation(program, "useTexture2"), false);
	
	gl.uniform1i(gl.getUniformLocation(program, "obj1"), false);
	gl.uniform1i(gl.getUniformLocation(program, "obj2"), false);
	gl.uniform1i(gl.getUniformLocation(program, "obj3"), false);
	gl.uniform1i(gl.getUniformLocation(program, "obj4"), true);
	
    gl.drawElements(gl.TRIANGLES, nFaces, gl.UNSIGNED_SHORT, 0);
	
	//Draw Cylinder Body
    gl.bindBuffer(gl.ARRAY_BUFFER, buf[0]);
    gl.vertexAttribPointer(vPosition, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);

    gl.bindBuffer(gl.ARRAY_BUFFER, buf[1]);
    gl.vertexAttribPointer(vNormal, 3, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vNormal);

    gl.bindBuffer(gl.ARRAY_BUFFER, buf[2]);
    gl.vertexAttribPointer(vUV, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vUV);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buf[3]);
	
    gl.drawElements(gl.TRIANGLES, nFaces, gl.UNSIGNED_SHORT, 0);
}

