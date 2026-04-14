#version 330
uniform sampler2D screen_texture;
in vec2 uv;
out vec4 fragColor;

vec2 crt_curve(vec2 uv) {
    uv = (uv - 0.5) * 2.0;
    uv.x *= 1.0 + pow(abs(uv.y) / 20.0, 2.0);
    uv.y *= 1.0 + pow(abs(uv.x) / 20.0, 2.0);
    uv = (uv / 2.0) + 0.5;
    return uv;
}

void main() {
    vec2 curved_uv = crt_curve(uv);

    if (curved_uv.x < 0.0 || curved_uv.x > 1.0 || curved_uv.y < 0.0 || curved_uv.y > 1.0) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }

    vec3 color = texture(screen_texture, curved_uv).rgb;

    float scanline = sin(curved_uv.y * 720.0 * 3.14159) * 0.01;
    color -= scanline;

    vec2 vig_uv = curved_uv * (1.0 - curved_uv.yx);
    float vignette = pow(vig_uv.x * vig_uv.y * 20.0, 0.15);
    color *= vignette;

    color *= vec3(0.95, 0.98, 1.05);

    fragColor = vec4(color, 1.0);
}