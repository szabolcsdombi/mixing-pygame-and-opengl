import sys

import pygame
import zengl

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

ctx = zengl.context()
image = ctx.image((800, 600), 'rgba8unorm')
pipeline = ctx.pipeline(
    vertex_shader="""
        #version 300 es
        precision highp float;

        vec2 vertex[4] = vec2[](
            vec2(-1.0, -1.0),
            vec2(-1.0, 1.0),
            vec2(1.0, -1.0),
            vec2(1.0, 1.0)
        );

        out vec2 uv;

        void main() {
            uv = vertex[gl_VertexID] * vec2(0.5, -0.5) + 0.5;
            gl_Position = vec4(vertex[gl_VertexID], 0.0, 1.0);
        }
    """,
    fragment_shader="""
        #version 300 es
        precision highp float;

        uniform sampler2D Texture;

        in vec2 uv;
        out vec4 out_color;

        void main() {
            out_color = texture(Texture, uv).bgra;
        }
    """,
    layout=[
        {
            "name": "Texture",
            "binding": 0,
        },
    ],
    resources=[
        {
            "type": "sampler",
            "binding": 0,
            "image": image,
            "min_filter": "nearest",
            "mag_filter": "nearest",
        },
    ],
    framebuffer=None,
    viewport=(0, 0, 800, 600),
    topology='triangle_strip',
    vertex_count=4,
)

display = pygame.surface.Surface((800, 600))
clock = pygame.time.Clock()

img = pygame.image.load('texture.png').convert()

while True:
    display.fill((0, 0, 0))
    display.blit(img, pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ctx.new_frame()
    image.write(display.get_buffer())
    pipeline.render()
    ctx.end_frame()
    pygame.display.flip()
    clock.tick(60)
