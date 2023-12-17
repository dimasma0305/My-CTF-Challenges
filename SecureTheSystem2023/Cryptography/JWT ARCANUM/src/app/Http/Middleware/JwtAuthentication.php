<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Config;

class JwtAuthentication
{
    private string $secretKey;
    private int $expiration;
    private string $cipher_algo;


    public function __construct()
    {
        $this->secretKey = Config::get('app.key');
        $this->cipher_algo = 'aes-128-gcm';
        $this->expiration = 3600;
    }

    public function handle(Request $request, Closure $next): JsonResponse|Response
    {
        if (isset($_COOKIE['jwt_token'])) {
            $token = $_COOKIE['jwt_token'];
            try {
                $decoded = $this->decode($token);
                if ($decoded['role'] === 'admin' && $decoded['isLogin']){
                    return $next($request);
                }
                return response()->json(['error'=>'Unauthorized'], 401);
            } catch (\Exception $e) {
                return response()->json(['error' => 'Unauthorized'], 401);
            }
        } else {
            return $this->generateToken(['role'=>'guest', 'secret'=>base64_encode(random_bytes(random_int(6,12))),'isLogin'=>false]);
        }
        return response()->json(['error' => 'Unauthorized'], 401);
    }

    /**
     * Generate a JWT token and set it in the response cookie.
     *
     * @param array $data
     * @return Response
     */
    public function generateToken(array $data): Response
    {
        $token = $this->encode($data);
        $response = new Response();
        $response->setContent('<meta http-equiv="refresh" content="0;url=/">');
        setcookie("jwt_token", $token);
        return $response;
    }

    /**
     * @throws RandomException
     */
    private function encode($data): string
    {
        $iv = random_bytes(12);
        $header = json_encode(['alg' => 'AES-128-GCM', 'typ' => 'JWT', 'iv' => base64_encode($iv)]);
        $payload = json_encode($data);
        $cipherText = openssl_encrypt($payload, $this->cipher_algo, $this->secretKey, 0, $iv, $tag);
        return base64_encode($header) .'.'. $cipherText .'.'. base64_encode($tag);
    }

    /**
     * @throws RandomException
     */
    private function decode($jwtToken): array
    {
        list($encodedHeader, $encodedCipherText, $encodedTag) = explode('.', $jwtToken);
        $header = json_decode(base64_decode($encodedHeader), true);
        $iv = base64_decode($header['iv']);
        $tag = base64_decode($encodedTag);
        $payload = openssl_decrypt($encodedCipherText, $this->cipher_algo, $this->secretKey, 0, $iv, $tag);
        return json_decode($payload, true);
    }
}
