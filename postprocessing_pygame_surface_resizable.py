import struct
import sys

import pygame
import zengl


class Postprocessing:
    def __init__(self, size):
        self.ctx = zengl.context()
        self.image = self.ctx.image(size, 'rgba8unorm')
        self.pipeline = self.ctx.pipeline(
            vertex_shader="""
                #version 300 es
                precision highp float;

                vec2 positions[3] = vec2[](
                    vec2(-1.0, -1.0),
                    vec2(3.0, -1.0),
                    vec2(-1.0, 3.0)
                );

                void main() {
                    gl_Position = vec4(positions[gl_VertexID], 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 300 es
                precision highp float;

                uniform sampler2D Texture;
                uniform ivec2 ScreenSize;

                layout (location = 0) out vec4 out_color;

                void main() {
                    ivec2 uv = ivec2(int(gl_FragCoord.x), ScreenSize.y - int(gl_FragCoord.y) - 1);
                    out_color = vec4(texelFetch(Texture, uv, 0).bgr, 1.0);
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
                    "image": self.image,
                },
            ],
            uniforms={
                'ScreenSize': size,
            },
            framebuffer=None,
            viewport=(0, 0, *size),
            topology='triangles',
            vertex_count=3,
        )

    def render(self, surface):
        size = surface.get_size()
        self.image.write(surface.get_view('1'), size)
        self.pipeline.uniforms['ScreenSize'][:] = struct.pack('2i', *size)
        self.pipeline.viewport = (0, 0, *size)
        self.ctx.new_frame()
        self.pipeline.render()
        self.ctx.end_frame()


pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.surface.Surface((800, 600))
clock = pygame.time.Clock()

img = pygame.image.load('texture.png').convert()

postprocessing = Postprocessing((800, 600))

while True:
    display.fill((0, 0, 0))
    display.blit(img, pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    postprocessing.render(display)
    pygame.display.flip()
    clock.tick(60)
