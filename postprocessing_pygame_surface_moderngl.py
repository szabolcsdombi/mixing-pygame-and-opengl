import sys

import pygame
import moderngl

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
ctx = moderngl.create_context()

program = ctx.program(
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
)

# program['Texture'] = 0
texture = ctx.texture((800, 600), 4)
vao = ctx.vertex_array(program, [], mode=moderngl.TRIANGLE_STRIP)
vao.scope = ctx.scope(textures=[(texture, 0)])
vao.vertices = 4

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

    ctx.clear()
    texture.write(display.get_buffer())
    vao.render()

    pygame.display.flip()
    clock.tick(60)
