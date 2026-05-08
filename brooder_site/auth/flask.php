<?php
// Flask API helper
// PHP never writes temperature data directly to MySQL.
// It calls the Flask API which handles all hardware-related data.

define('FLASK_URL', 'https://your-render-url.onrender.com');  // update after deploying to Render
define('FLASK_KEY', 'your-brooder-api-key');                   // from the brooders table

/**
 * Call the Flask API
 * @param string $method  GET or POST
 * @param string $endpoint  e.g. /api/settings
 * @param array  $body    data to send as JSON (POST only)
 * @return array          decoded JSON response
 */
function flask_call($method, $endpoint, $body = []) {
    $ch = curl_init(FLASK_URL . $endpoint);

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . FLASK_KEY
    ]);

    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
    }

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    return [
        'status' => $httpCode,
        'data'   => json_decode($response, true)
    ];
}
