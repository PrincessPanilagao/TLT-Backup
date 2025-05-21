    ##################################
    #   Mini Game (Bia's room):      #
    #     Connect the Mirrors        #
    #   cr: connect pipes tutorial   #
    ##################################


transform rotate_pipe:
    rotate 10
    rotate_pad False

transform fadein_bg:
    alpha 0.0
    linear 0.5 alpha 1.0
    
    
# CM BIA GAME (4x4 game)
default pipe_rows = 4
default pipe_columns = 4
default amount_of_pipes = pipe_rows * pipe_columns # total amt of pipes in the mini-game
default grid_path = [] # a list that will be filled with cells of the grid which forms a path from start to end
default pipes = [] # a list that will be filled with list items containing information about each pipe in the game
default pipe_types = {"straight" : ("top", "bottom"), "curved" : ("right", "bottom")}
default connected_pipes = [] # keeps a track of the pipes that have been strung together

init python:
    # Connect mirror game
    def setup_pipe_game():
        # Function which sets up the pipe mini-game
        global pipes
        global connected_pipes
        # Reset the pipes and connected_pipes list to empty lists
        pipes = []
        connected_pipes = []
        # Generate a grid path from start to end 
        generate_grid_path()
        # Fill the pipes list with pipes after generating a grid path
        create_pipes()

    def create_pipes():
        for i in range(1, amount_of_pipes + 1):
            if i == 1:
                # Create the first pipe in the grid
                if grid_path[0] + 1 == grid_path[1]:
                    create_pipe(type="straight", cell=i)
                elif grid_path[0] + pipe_columns == grid_path[1]:
                    create_pipe(type="curved", cell=i)

            elif i == amount_of_pipes:
                # Last pipe in the grid
                current_cell_index = grid_path.index(i)
                if grid_path[current_cell_index] - 1 == grid_path[-2]:
                    create_pipe(type="straight", cell=grid_path[current_cell_index])
                else:
                    create_pipe(type="curved", cell=grid_path[current_cell_index])

            elif i in grid_path:
                # Cell is part of the path
                current_cell_index = grid_path.index(i)
                next_cell_index = current_cell_index + 1
                prev_cell_index = current_cell_index - 1

                if grid_path[current_cell_index] % pipe_columns == 1:
                    # First in its row
                    if grid_path[current_cell_index] + 1 == grid_path[next_cell_index]:
                        create_pipe(type="curved", cell=grid_path[current_cell_index])
                    elif grid_path[current_cell_index] + pipe_columns == grid_path[next_cell_index]:
                        create_pipe(type="straight", cell=grid_path[current_cell_index])

                elif grid_path[current_cell_index] % pipe_columns == 0 and grid_path[current_cell_index] <= pipe_columns:
                    # Last in row 1
                    create_pipe(type="curved", cell=grid_path[current_cell_index])

                elif grid_path[current_cell_index] % pipe_columns == 0 and grid_path[current_cell_index] > pipe_columns:
                    # Last in rows below the first
                    if grid_path[current_cell_index] - pipe_columns == grid_path[prev_cell_index]:
                        create_pipe(type="straight", cell=grid_path[current_cell_index])
                    elif grid_path[current_cell_index] - 1 == grid_path[prev_cell_index]:
                        create_pipe(type="curved", cell=grid_path[current_cell_index])

                else:
                    # In-between cell
                    if grid_path[current_cell_index] <= pipe_rows:
                        # First row
                        if grid_path[current_cell_index] + 1 == grid_path[next_cell_index]:
                            create_pipe(type="straight", cell=grid_path[current_cell_index])
                        elif grid_path[current_cell_index] + pipe_columns == grid_path[next_cell_index]:
                            create_pipe(type="curved", cell=grid_path[current_cell_index])

                    elif grid_path[current_cell_index] >= amount_of_pipes - pipe_columns:
                        # Last row
                        if grid_path[current_cell_index] - pipe_columns == grid_path[prev_cell_index]:
                            create_pipe(type="curved", cell=grid_path[current_cell_index])
                        elif grid_path[current_cell_index] - 1 == grid_path[prev_cell_index]:
                            create_pipe(type="straight", cell=grid_path[current_cell_index])

                    else:
                        # Middle rows
                        if grid_path[current_cell_index] - 1 == grid_path[prev_cell_index]:
                            if grid_path[current_cell_index] + 1 == grid_path[next_cell_index]:
                                create_pipe(type="straight", cell=grid_path[current_cell_index])
                            elif grid_path[current_cell_index] + pipe_columns == grid_path[next_cell_index]:
                                create_pipe(type="curved", cell=grid_path[current_cell_index])
                        elif grid_path[current_cell_index] - pipe_columns == grid_path[prev_cell_index]:
                            if grid_path[current_cell_index] + 1 == grid_path[next_cell_index]:
                                create_pipe(type="curved", cell=grid_path[current_cell_index])
                            elif grid_path[current_cell_index] + pipe_columns == grid_path[next_cell_index]:
                                create_pipe(type="straight", cell=grid_path[current_cell_index])

            else:
                # Cell is not in the path, add a random pipe
                random_type = renpy.random.choice(list(pipe_types.keys()))
                create_pipe(type=random_type, cell=i)
            
        # elif i == amount_of_pipes:
        #     # Last run of the loop
        #     # We add the last pipe into the last cell of the grid
        #     current_cell_index = grid_path.index(i)
        #     if grid_path[current_cell_index] - 1 == grid_path[-2]:
        #         # The previous cell was to the left
        #         # This cell needs a straight pipe
        #         create_pipe(type = "straight", cell = grid_path[current_cell_index])
        #     else:
        #         # The previous cell was above
        #         # This cell needs a curved pipe
        #         create_pipe("curved", cell = grid_path[current_cell_index])

    def create_pipe(type, cell):
        # Function that creates information about an individual pipe
        pipe_image = "images/biasroom/cm/%s-pipe.png" % type # Create the image-path to the pipe
        pipe_end_points = list(pipe_types[type]) # get all the end-points the pipe type has
        final_pipe = [pipe_image, type, pipe_end_points, cell, 0] # 1: image, 2: typ of pipe, 3: its end-points, 4: which
        pipes.append(final_pipe) # Add the final tuple "final_pipe" into the "pipes" list

    def generate_grid_path():
        global grid_path
        # Function to generate a path of cells in the grid from start to end where the path might lead: right or down
        # This path will be ONE valid way of connecting the pipes
        grid_path = [1]
        for i in range(pipe_columns + pipe_rows - 2):
            if grid_path[-1] % pipe_columns == 0 and grid_path[-1] <= amount_of_pipes - pipe_columns:
                # The previous cell in the path list is in te last column, but not in the last row
                # The following cell can only be below
                grid_path.append(grid_path[-1] + pipe_columns)
            
            elif grid_path[-1] % pipe_columns != 0 and grid_path[-1] <= amount_of_pipes - pipe_columns:
                # The previous cell is before the last column, and not in the last row
                # This cell can be followed by a cell to the right or below
                potential_cells = ["right", "down"]
                random_pick = renpy.random.choice(potential_cells)
                if random_pick == "right":
                    grid_path.append(grid_path[-1] + 1)
                elif random_pick == "down":
                    grid_path.append(grid_path[-1] + pipe_columns)
            
            elif grid_path[-1] > amount_of_pipes - pipe_columns:
                # The previous cell is in the last row
                # The following cell can only be to the right
                grid_path.append(grid_path[-1] + 1)
    
    def update_pipe_endpoints(cell):
        # After a pipe has been rotated, we need to update its endpoint values to reflect the change
        for pipe in pipes:
            if pipe[3] == cell:
                for endpoint in pipe[2]:
                    # Loop through its endpoints
                    if endpoint == "top":
                        # The current endpoint is "top", so we change it to "right"
                        endpoint_index = pipe[2].index("top")
                        pipe[2][endpoint_index] = "right"
                    elif endpoint == "right":
                        # The current endpoint is "right", so we change it to "bottom"
                        endpoint_index = pipe[2].index("right")
                        pipe[2][endpoint_index] = "bottom"
                    elif endpoint == "bottom":
                        # The current endpoint is "bottom", so we change it to "left"
                        endpoint_index = pipe[2].index("bottom")
                        pipe[2][endpoint_index] = "left"
                    elif endpoint == "left":
                        # The current endpoint is "left", so we change it to "top"
                        endpoint_index = pipe[2].index("left")
                        pipe[2][endpoint_index] = "top"
                break

    def rotate_pipe(cell):
        # Function that changes the rotation of a pipe in the pipes list, according to its position/cell
        # We're NOT actually rotating a pipe imagebutton here, just setting a value in the pipes list
        if pipes[cell -1][4] == 360:
            pipes[cell - 1][4] = 90
        else:
            pipes[cell - 1][4] += 90
        
        renpy.sound.play("audio/sfx/mirrorlight/lightmove.mp3", loop=False)
        renpy.sound.set_volume(0.1)
        update_pipe_endpoints(cell)
        check_pipe_connections()
    
    def check_pipe_connections():
        # Function that checks if there's a path with aligned pipes from the starting point to the ending point in the grid
        global connected_pipes
        connected_pipes = []
        if "left" in pipes[0][2] and pipes[0] not in connected_pipes:
            # The first pipe in the grid is connected to its starting point so we add it to the connected_pipes list
            connected_pipes.append(pipes[0])
        
        if len(connected_pipes) > 0 and connected_pipes[0][3] == 1:
            # The connected_pipes list contains the first pipe in the grid
            # That means we can now check if the first pipe has an endpoint that aligns with another pipe
            for pipe in connected_pipes:
                pipe_to_add = None
                if pipe[3] % pipe_columns == 1 and pipe[3] != 1 and "left" in pipe[2]:
                    # Current pipe in the loop is the first one in its row but not the first in the grid
                    # It has a loose left endpoint where liquid could pour out, so we break the loop
                    break
                
                if pipe[3] % pipe_columns != 0:
                    # Current pipe in the loop is not the last one in its row
                    if "right" in pipe[2]:
                        if "left" in pipes[pipe[3]][2]:
                            # This pipe aligns with a pipe to the left of it
                            if pipes[pipe[3]] not in connected_pipes:
                                pipe_to_add = pipes[pipe[3]]
                        else:
                            # The pipe has a loose right endpoint and can't be used
                            break

                if pipe[3] <= amount_of_pipes - pipe_columns:
                    # Current pipe in the loop is not in the last row
                    if "bottom" in pipe[2]:
                        if "top" in pipes[pipe[3] - 1 + pipe_columns][2]:
                            # This pipe aligns with a pipe below it
                            if pipes[pipe[3] - 1 + pipe_columns] not in connected_pipes:
                                pipe_to_add = pipes[pipe[3] - 1 + pipe_columns]
                        else:
                            break
                
                elif pipe[3] > amount_of_pipes - pipe_columns and "bottom" in pipe[2]:
                    # Current pipe in the loop is in the last row and it has a loose bottom endpoint
                    break
                
                if pipe[3] > pipe_columns:
                    # Current pipe in the loop is not in the first row
                    if "top" in pipe[2]:
                        if "bottom" in pipes[pipe[3] - 1 - pipe_columns][2]:
                            # The pipe aligns with the pipe above it
                            if pipes[pipe[3] - 1 - pipe_columns] not in connected_pipes:
                                pipe_to_add = pipes[pipe[3] - 1 - pipe_columns]
                        else:
                            break
                
                elif pipe[3] <= pipe_columns and "top" in pipe[2]:
                    # Current pipe in the loop is in the first row and it has a loose top endpoint
                    break
                
                if pipe[3] % pipe_columns != 1 and pipe[3] != amount_of_pipes:
                    # Current pipe in the loop is not the first in its row and is not the last one in the grid
                    if "left" in pipe[2]:
                        if "right" in pipes[pipe[3] - 2][2]:
                            # The pipe aligns with the pipe to the left of it
                            if pipes[pipe[3] - 2] not in connected_pipes:
                                pipe_to_add = pipes[pipe[3] - 2]
                        else:
                            break
                
                if pipe_to_add != None:
                    # When the current pipe has no loose endpoint
                    connected_pipes.append(pipe_to_add)
        
        if len(connected_pipes) > 0:
            if amount_of_pipes == connected_pipes[-1][3]:
                if "right" not in connected_pipes[-1][2]:
                    connected_pipes.pop(-1)
                else: # WHEN GAME IS SUCCESSFUL
                    renpy.sound.play("audio/sfx/mirrorlight/lightcorrect.mp3", loop=False)
                    renpy.sound.set_volume(0.3)
                    renpy.jump("after_cm")


# Connect the pipe screen w/ imagebuttons
screen connect_the_pipes:
    # image "images/backgrounds/act 2/bg cmdark.png"

    # Objective 
    add "images/objectives/objective connectlight.png" zoom 1.0 xalign 0.0 yalign 0.1 xoffset -30 at slide_in_pause_out

    grid pipe_columns pipe_rows:
        at fadein_bg
        spacing 0
        pos (640, 140)
        anchor(0.0, 0.0)
        for pipe in pipes:
            if pipe in connected_pipes:
                imagebutton idle Transform("images/biasroom/cm/" + pipe[1] + "-pipe-connected.png", rotate = pipe[4], rotate_pad = False) action Function(rotate_pipe, cell = pipe[3])
            else:
                imagebutton idle Transform(pipe[0], rotate = pipe[4], rotate_pad = False) action Function(rotate_pipe, cell = pipe[3])