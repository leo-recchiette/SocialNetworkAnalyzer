<?php
    // Base directory containing the Python backend (the `server/` folder lives
    // next to this file). Previously the scripts were invoked via a hardcoded
    // "'.$SNA_BASE.'/server/..." path; deriving it from __DIR__ makes the app
    // relocatable and lets it run unchanged inside the Docker image, where it
    // lives at /var/www/html. Override with the SNA_BASE env var if needed.
    $SNA_BASE = getenv('SNA_BASE') ?: __DIR__;

    class config {
        public function __construct($value, $user_name)
        {
            $this->value = $value;
            $this->user_mail = $user_name;
        }
    }

    function rrmdir($dir)
    {
        if (is_dir($dir))
        {
            $objects = scandir($dir);
            foreach ($objects as $object)
            {
                if ($object != '.' && $object != '..')
                {
                    if (is_dir($dir.'/'.$object) && !is_link($dir.'/'.$object))
                        rrmdir($dir.'/'.$object);
                    else
                        unlink($dir.'/'.$object);
                }
            }
            rmdir($dir);
        }
    }

    // to login or register
    if (isset($_POST['user']) && isset($_POST['pass']) && isset($_POST['action']) )
    {
        $user = escapeshellarg($_POST['user']);
        $pass = escapeshellarg($_POST['pass']);
        $action = $_POST['action'];

        $output = shell_exec('python '.$SNA_BASE.'/server/userManagement.py '. $user.' '. $pass .' \''.$action.'\' 2>&1');

        if ($action == 'login')
        {
            if ($output==1 ) {
                mkdir('uploads/' . $_POST['user'], 0777);
                $config = new config(1, $_POST['user'] );
                echo json_encode($config);
            }
            else if ($output== -1 ){
                $config = new config(-1, $_POST['user'] );
                echo json_encode($config);
            }
            else if ($output== 0){
                $config = new config(0, 'Insert a valid mail' );
                echo json_encode($config);
            }
        }
        else if ($action == 'register')
        {
            if ($output==1 )
            {
                $config = new config(1, 'Mail already used' );
                echo json_encode($config);
            }
            else if ($output== 0){
                $config = new config(0, 'Now you can login' );
                echo json_encode($config);
            }
        }

    }

    //get the values for the sliders
    if (isset($_POST['usr']) && isset($_POST['sn']) )
    {
        $user = escapeshellarg($_POST['usr']);
        $sn = escapeshellarg($_POST['sn']);
        // graphType scopes the node/edge slider maxima to the current view
        // (relNet = people, trafficNet = content); default relNet if absent.
        $graphType = escapeshellarg(isset($_POST['graphType']) ? $_POST['graphType'] : 'relNet');

        $output = shell_exec('python '.$SNA_BASE.'/server/getValueForSearching.py '. $user.' '. $sn .' '. $graphType .' 2>&1');

        echo $output;
    }

    //change mail or pass
    if (isset($_POST['usr']) && isset($_POST['typedValue']) && isset($_POST['action']) ) {
        $user = escapeshellarg($_POST['usr']);
        $typedValue = escapeshellarg($_POST['typedValue']);
        $action = $_POST['action'];

        $output = shell_exec('python '.$SNA_BASE.'/server/userManagement.py '. $user.' '. $typedValue .' \''.$action.'\' 2>&1');

        if ($action == 'change-mail')
        {
            $config = new config('Mail changed', $_POST['typedValue'] );
            echo json_encode($config);
        }
        else
        {
            $config = new config('Password changed',  $typedValue );
            echo json_encode($config);
        }
    }

    // upload file on server
    if (isset($_FILES['file']) && $_POST['user']!='' && isset($_POST['wordFrecOption']))
    {
        if ( 0 < $_FILES['file']['error'] ) {
            echo 'Error: ' . $_FILES['file']['error'] . '<br>';
        }
        else {
            $errors = [];
            $file_name = reset(explode('.', $_FILES['file']['name']));
            $file_ext = end(explode('.', $_FILES['file']['name']));
            $valid_ext = array('zip', 'mbox');
            $wordFrecOption = escapeshellarg($_POST['wordFrecOption']);

            if (!in_array($file_ext, $valid_ext))
                $errors[] = 'File not allowed';
            else{
                if ($_FILES['file']['size'] > 524288000) {
                    $errors[] = 'File size exceeds limit';
                }

                if (empty($errors)) {
                    $path = 'uploads/'.$_POST['user'].'/'.$file_name;
                    mkdir($path, 0777, true);
                    move_uploaded_file($_FILES['file']['tmp_name'], $path.'/'.$_FILES['file']['name']);
                }

                if ($file_ext == 'zip'){
                    if (strpos( $_FILES['file']['name'], 'facebook') !== false){
                        $output = shell_exec('python '.$SNA_BASE.'/server/dumper/fbDumpUploader.py '.$path.' '.$_POST['user'].' '.$wordFrecOption.' 2>&1');
                        echo $output;
                    }
                    else if (strpos( $_FILES['file']['name'], 'twitter') !== false){
                        $output = shell_exec('python '.$SNA_BASE.'/server/dumper/twitterDumpUploader.py '.$path.' '.$_POST['user'].' '.$wordFrecOption.' 2>&1');
                        echo $output;
                    }
                }
                else if ($file_ext == 'mbox'){
                    require_once 'Mail/Mbox.php';  // include Pear.Mail_Mbox module (installaton  of Pear-> https://pear.php.net/manual/en/installation.getting.php)
                    require_once 'Mail/mimeDecode.php'; // include Pear.Mail_MimeDecode
                    $f2open = $path.'/'.$_FILES['file']['name'];
                    $mbox = new Mail_Mbox($f2open);
                    $mbox->open();
                    $message = $mbox->get(0);
                    $decodedMessage = new Mail_mimeDecode($message, '\r\n');
                    $structuredMessage = $decodedMessage->decode(
                        array(
                            'decode_headers'    =>  true,
                            'include_bodies'    =>  true,
                            'decode_bodies'     =>  true
                        )
                    );
                    $sender = $structuredMessage->headers['from'];
                    $mbox->close();
                    $output = shell_exec('python '.$SNA_BASE.'/server/dumper/mboxDumpUploader.py getNodesEdges '.$path.'/'.$_FILES['file']['name'].' '.$sender.' '.$_POST['user'].' '.$wordFrecOption.' 2>&1');
                    echo $output;
                }
                rrmdir($path);
            }
        }
    }

    // delete dump on server
    if (isset($_POST['usr']) && isset($_POST['valueToDelete']))
    {
        $valueToDelete = $_POST['valueToDelete'];
        $usr = $_POST['usr'];
        $cmd = 'python -W ignore '.$SNA_BASE.'/server/menageDumps.py '.$usr.' '.$valueToDelete.' 2>&1';
        $output = shell_exec($cmd);
        echo $output;
    }

    //get data from server
    if (isset($_POST['dataToSearch']))
    {
        if (isset($_POST['id']))
        {
            $dataToSearch = escapeshellarg($_POST['dataToSearch']);
            $id = escapeshellarg($_POST['id']);

            $cmd = 'python -W ignore '.$SNA_BASE.'/server/dataSearcher/getData.py '.$dataToSearch.' '.$id.' 2>&1';
            $output = shell_exec($cmd);
            echo $output;
        }
        else if (isset($_POST['lat']) && isset($_POST['lng']))
        {
            $dataToSearch = escapeshellarg($_POST['dataToSearch']);
            $lat = escapeshellarg($_POST['lat']);
            $lng = escapeshellarg($_POST['lng']);

            $cmd = 'python -W ignore '.$SNA_BASE.'/server/dataSearcher/getData.py '.$dataToSearch.' '.$lat.' '.$lng.' 2>&1';
            $output = shell_exec($cmd);
            echo $output;
        }
        else if (isset($_POST['action']) && $_POST['action'] == 'getMarker')
        {
            $dataToSearch = escapeshellarg($_POST['dataToSearch']);

            $cmd = 'python -W ignore '.$SNA_BASE.'/server/dataSearcher/getMarkerForMap.py '.$dataToSearch.' '.$_POST['markersToDisplay'].' 2>&1';
            $output = shell_exec($cmd);
            echo $output;
        }
        else if (isset($_POST['action']) && $_POST['action'] == 'getData' )
        {
            $dataToSearch = escapeshellarg($_POST['dataToSearch']);

            $cmd = 'python -W ignore '.$SNA_BASE.'/server/dataSearcher/getData.py '.$dataToSearch.' '.$_POST['ntd'].' 2>&1';
            $output = shell_exec($cmd);
            echo $output;
        }
        else if (isset($_POST['action']) && $_POST['action'] == 'getTimelineObject' )
        {
             $dataToSearch = escapeshellarg($_POST['dataToSearch']);

             $cmd = 'python -W ignore '.$SNA_BASE.'/server/dataSearcher/getTimelineObject.py '.$dataToSearch.' 2>&1';
             $output = shell_exec($cmd);
             echo $output;
        }
        else if (isset($_POST['action']) && $_POST['action'] == 'getSingleWordsFrequencyContent' )
        {
             $dataToSearch = escapeshellarg($_POST['dataToSearch']);
             $word = escapeshellarg($_POST['word']);

             $cmd = 'python -W ignore '.$SNA_BASE.'/server/dataSearcher/getSingleWordsFrequencyContent.py '.$dataToSearch.' '.$word.' 2>&1';
             $output = shell_exec($cmd);
             echo $output;
        }

    }

    // run a Cypher query (built by the frontend's allQueries.js) and return the
    // resulting graph as {nodes, rels} JSON for the Sigma.js visualization. This
    // replaces neovis.js's direct browser->bolt connection: the DB password now
    // stays server-side (in dbConnector via the environment) instead of shipping
    // to every browser.
    if (isset($_POST['action']) && $_POST['action'] == 'runQuery' && isset($_POST['cmd']))
    {
        $cmd = escapeshellarg($_POST['cmd']);
        $output = shell_exec('python -W ignore '.$SNA_BASE.'/server/dataSearcher/runVizQuery.py '.$cmd.' 2>&1');
        echo $output;
    }
