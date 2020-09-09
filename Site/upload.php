<?php

$arg1 = $_GET['a1']; // Name
$arg1 = preg_replace('/_.*/','',$arg1);
$arg1 = basename($arg1);

$target_dir = "/srv/users/maximeme/apps/drawyourmeme/public/Upload/";
$target_file = $target_dir . basename($_FILES["file"]["name"]);
$uploadOk = 1;
$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);

// Check if image file is a actual image or fake image
$check = getimagesize($_FILES["file"]["tmp_name"]);
if($check !== false) {  
    $uploadOk = 1; 
	} else {
    echo "File is not an image.";
    $uploadOk = 0;
}

// Check if fiddled with name
if(!preg_match("/^[a-zA-Z0-9]{20}$/",$arg1)){
$uploadOk = 0;
echo "Looks like the new name got changed. File wont get uploaded.";
}

// Check if file already exists
if (file_exists($target_file)) {
    echo "Sorry, file already exists. ";
    $uploadOk = 0;
}
// Check file size (5Mb)
if ($_FILES["file"]["size"] > 5000000) {
    echo "Sorry, your file is too large. 5MB maximum.";
    $uploadOk = 0;
}
// Allow certain file formats
if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg" && $imageFileType != "J" && $imageFileType != "PNG"
&& $imageFileType != "gif" ) {
    echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed. " .$imageFileType . "    ";
    $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
    return -1;
// if everything is ok, try to upload file
}else {
    if (move_uploaded_file($_FILES["file"]["tmp_name"], $target_dir . $arg1. ".png")) {
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
?>