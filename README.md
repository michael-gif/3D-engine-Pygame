# 3D-engine-Pygame
A 3D game engine that uses only pygame

## Goals
- Make a 3d game engine that can render shapes made of triangles.  
- Have collisions for the shapes.  
- Possibly add lighting.

## Usage
add shapes to the `shapes` list:  

syntax|example
---|---
`box(width,length,height,(x,y,z))`|`box(5,5,5,(0,0,0))`
`triangle((x,y,z))`|`triangle((0,0,0))`

so adding a box to the list would look like:  
`shapes = [box(0,0,0,(0,0,0))]`
