<?php
$datetime = date('d-m-Y-H\hi');

if (!is_dir("LOL")) {
    mkdir("LOL", 0777, true);
}

if (!file_exists('.htaccess')) {
    $text = <<<EOT
# Ceci refuse l'accès à n'importe quel fichier dans un dossier lui-même dans un dossier
# il bloque donc l'accès direct aux fichiers d'un projet sans bloquer les fichiers d'un utilisateur comme son logo
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{REQUEST_URI} ^.*/[^/]+/[^/]+/[^/]+/.+$
    RewriteRule ^ - [F,L]
</IfModule>

Options -Indexes
EOT;
    file_put_contents('.htaccess', $text);
}

if (!file_exists('LOL/.htaccess')) {
    copy('.htaccess', 'LOL/.htaccess');
}

if (isset($_POST['data'])) {
    $data = $_POST['data'];
    $title_file = $_POST['title_file'];
    $folder_name = $_POST['folder_name'] . "_" . $datetime;

    if (!is_dir("LOL/$folder_name")) {
        mkdir("LOL/$folder_name", 0777, true);
    }

    if (!file_exists("LOL/$folder_name/.htaccess")) {
        copy('.htaccess', "LOL/$folder_name/.htaccess");
    }

    if (!empty($data)) {
        $decodedData = json_decode($data, true);

        if ($decodedData !== null) {
            $filePath = "LOL/$folder_name/$title_file.json";
            file_put_contents($filePath, json_encode($decodedData, JSON_PRETTY_PRINT)); // Sauvegarde dans le fichier .json
        }
    }
}

if (isset($_POST['infos'])) {
    $infos = $_POST['infos'];
    $title_file_infos = $_POST['title_file_infos'];
    $folder_name_infos = $_POST['folder_name_infos'] . "_" . $datetime;

    if (!is_dir("LOL/$folder_name_infos")) {
        mkdir("LOL/$folder_name_infos", 0777, true);
    }

    if (!file_exists("LOL/$folder_name_infos/.htaccess")) {
        copy('.htaccess', "LOL/$folder_name_infos/.htaccess");
    }

    if (!empty($infos)) {
        $decodedInfos = json_decode($infos, true);

        if ($decodedInfos !== null) {
            $filePath = "LOL/$folder_name_infos/$title_file_infos.txt";
            file_put_contents($filePath, json_encode($decodedInfos, JSON_PRETTY_PRINT)); // Sauvegarde dans le fichier .txt
        }
    }
}

exit();
?>
