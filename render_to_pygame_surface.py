import sys

import pygame
import zengl

zengl.init(zengl.loader(headless=True))

pygame.init()

screen = pygame.display.set_mode((800, 600))
display = pygame.surface.Surface((800, 600))
clock = pygame.time.Clock()

img = pygame.surface.Surface((300, 300), pygame.SRCALPHA)

ctx = zengl.context()
image = ctx.image((300, 300), 'rgba8unorm')
image.clear_value = (0.0, 0.0, 0.0, 0.0)
pipeline = ctx.pipeline(
    vertex_shader="""
        #version 300 es
        precision highp float;

        out vec3 v_color;

        vec2 positions[3] = vec2[](
            vec2(0.0, 1.0),
            vec2(-0.866, -0.5),
            vec2(0.866, -0.5)
        );

        vec3 colors[3] = vec3[](
            vec3(1.0, 0.0, 0.0),
            vec3(0.0, 1.0, 0.0),
            vec3(0.0, 0.0, 1.0)
        );

        void main() {
            gl_Position = vec4(positions[gl_VertexID], 0.0, 1.0);
            v_color = colors[gl_VertexID];
        }
    """,
    fragment_shader="""
        #version 300 es
        precision highp float;

        in vec3 v_color;

        layout (location = 0) out vec4 out_color;

        void main() {
            out_color = vec4(v_color, 1.0);
            out_color.rgb = pow(out_color.rgb, vec3(1.0 / 2.2));
        }
    """,
    framebuffer=[image],
    topology="triangles",
    vertex_count=3,
)

while True:
    display.fill((0, 0, 0))

    image.clear()
    pipeline.render()
    img.get_buffer().write(image.read())

    display.blit(img, (200, 200))
    display.blit(img, pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(display, (0, 0))
    pygame.display.flip()
    clock.tick(60)
