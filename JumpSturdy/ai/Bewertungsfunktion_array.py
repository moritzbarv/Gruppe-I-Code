
#Bewertungsfunktion 

def evaluate_position(position, color, maximizingP): 
    	
    player_pieces = 0
    opponent_pieces = 0

    position_bonus_blue = 0
    position_bonus_red = 0

    blue_pieces = 0
    red_pieces = 0

    #Anzahl Pieces
    for row in position:
        for col in row:
            if col == 'R':    
                red_pieces += 1
            if col == 'RR':
                red_pieces += 2
            if col == 'B' :
                blue_pieces += 1
            if col == 'BB' :
                blue_pieces += 2    
            if col == 'RB' :
                red_pieces += 1
                blue_pieces +=1 
            if col == 'BR' :
                red_pieces += 1
                blue_pieces +=1 
    
    if red_pieces == 1 and blue_pieces > 1:
        position_bonus_red -= 2
    if blue_pieces == red_pieces > 1 :
        position_bonus_blue -= 2

    #Wer ist als nächstes dran
    next = ''

    if maximizingP == False and color == 'red':
        next = 'blue'
    if maximizingP == True and color == 'red':
        next = 'red'
    if maximizingP == False and color == 'blue':
        next = 'red'
    if maximizingP == True and color == 'blue':
        next = 'blue'        
    
    #Vorsprung Pieces
    if red_pieces == 12 and blue_pieces == 11 :
        position_bonus_red += 2
    if blue_pieces == 12 and red_pieces == 11 : 
        position_bonus_blue += 2

    if red_pieces >= blue_pieces+2 :
        position_bonus_red += 3
    if blue_pieces >= red_pieces+2 :
        position_bonus_blue += 3


    #Näher dran am Ziel
    closest_red_top = None
    closest_blue_top = None
    double_jump_red = False
    double_jump_blue = False

    for row_idx, row in enumerate(position):
        for col_idx, cell in enumerate(row):
            if cell == 'R' or cell == 'RR' or cell == 'BR':
                closest_red_top = row_idx
                break
        if closest_red_top is not None:
            break   

    for row_idx, row in enumerate(position):
        for col_idx, cell in enumerate(row):
            if cell == 'B' or cell == 'BB' or cell == 'RB':
                closest_blue_top = row_idx
                if cell == 'BB' or cell == 'RB': 
                    double_jump_blue = True
                break
        if closest_blue_top  is not None:
            break 
    
    closest_red_bottom = None
    closest_blue_bottom = None

    for row_idx, row in enumerate(reversed(position)):
        for col_idx, cell in enumerate(row):
            if cell == 'R' or cell == 'RR' or cell == 'BR':
                closest_red_bottom = row_idx
                if cell == 'RR' or cell == 'BR':
                    double_jump_red = True
                    
                break
        if closest_red_bottom is not None:
            break

    for row_idx, row in enumerate(reversed(position)):
        for col_idx, cell in enumerate(row):
            if cell == 'B' or cell == 'BB' or cell == 'RB':
                closest_blue_bottom = row_idx
                break
        if closest_blue_bottom is not None:
            break

    if closest_red_top != None and closest_red_bottom != None and closest_blue_top != None and closest_blue_bottom != None:
        if closest_blue_top == closest_red_bottom :  
                
            if next == 'blue' : 
                if double_jump_red == False and (double_jump_blue == False or double_jump_blue == True): 
                    position_bonus_blue += 5
                if double_jump_red == True and double_jump_blue == True: 
                    position_bonus_blue += 5
                if double_jump_red == True and double_jump_blue == False : 
                    position_bonus_blue -= 5

            if next == 'red' : 
                if double_jump_blue == False and (double_jump_red == False or double_jump_red == True): 
                    position_bonus_red += 5
                if double_jump_blue == True and double_jump_red == True: 
                    position_bonus_red += 5
                if double_jump_blue == True and double_jump_red == False : 
                    position_bonus_red -= 5    

        if closest_blue_top <= closest_red_top :          
            position_bonus_blue += 5
        if closest_red_bottom <= closest_blue_bottom :          
            position_bonus_red += 5

        if closest_red_bottom <  closest_blue_top and closest_red_bottom <= closest_blue_bottom and double_jump_blue == False: 
            position_bonus_red += 10
        if closest_blue_top < closest_red_bottom and closest_blue_top <= closest_red_top and double_jump_red == False: 
            position_bonus_blue += 10 
	
	
	
    if blue_pieces == 0 : 
        position_bonus_blue -= 500

    if red_pieces == 0 : 
        position_bonus_red -= 500
    
    blue_distances = 0
    red_distances = 0

    if red_pieces != 0 and blue_pieces != 0:
        for row_idx, row in enumerate(position):
            for cell in enumerate(row):
                if cell[1] == 'R':
                    red_distances += len(position) - 1 - row_idx  
                elif cell[1] == 'RR':
                    red_distances += (len(position) - 1 - row_idx) *1 - 1
                elif cell[1] == 'B':
                    blue_distances += row_idx  
                elif cell[1] == 'BB':
                    blue_distances += row_idx*2 -1
    
    if blue_distances  < red_distances : 
        position_bonus_blue += 1
        if blue_distances + 2  < red_distances : 
            position_bonus_blue += 2
    elif red_distances  < blue_distances :
        position_bonus_red += 1
        if red_distances + 2  < blue_distances : 
            position_bonus_blue += 2    

    #Bonus Punkte: Schlagen/Gefahr oder kurz vorm Ziel
    for row_idx, row in enumerate(position):
        for col_idx, cell in enumerate(row):
            if next == 'red' :
                if cell == 'R' :
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and (position[row_idx + 1][col_idx-1] == 'B' or position[row_idx+1][col_idx+1] == 'B'): 
                        position_bonus_red -= 1
                        if red_pieces == 1 and blue_pieces > 1 :
                            position_bonus_red -= 10
                    if row_idx < len(position) -1 and col_idx + 1> 0 and col_idx < len(row) - 2 and(position[row_idx + 1][col_idx-2] in ['RB', 'BB'] or position[row_idx + 1][col_idx+2] in ['RB', 'BB']):
                        position_bonus_red -= 1
                        if red_pieces == 1 and blue_pieces > 1:
                            position_bonus_red -= 10
                    if row_idx < len(position) -2 and col_idx > 0 and col_idx < len(row) - 1 and(position[row_idx + 2][col_idx-1] in ['RB', 'BB'] or position[row_idx + 2][col_idx +1] in ['RB', 'BB']):
                        position_bonus_red -= 1   
                        if red_pieces == 1 and blue_pieces > 1:
                            position_bonus_red -= 10
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and red_pieces == 1 and blue_pieces == 1 and position[row_idx + 1][col_idx] == 'B':
                        position_bonus_red -= 50
                    if row_idx < len(position) -1 and row_idx == 6 : 
                        position_bonus_red += 1
                        if row_idx == 6 and col_idx == 0 and position[row_idx + 1][col_idx + 1] in ['B','BB'] :
                            position_bonus_red += 50
                        if row_idx == 6 and col_idx == 7 and position[row_idx + 1][col_idx - 1] in ['B','BB'] :
                            position_bonus_red += 50
                        if row_idx == 6 and col_idx + 2 > 0 and col_idx < len(row) - 2 and position[row_idx + 1][col_idx-1] != 'B' and position[row_idx+1][col_idx+1] != 'B' and position[row_idx + 1][col_idx-2] not in ['RB', 'BB'] and position[row_idx + 1][col_idx+2] not in ['RB', 'BB']: 
                            position_bonus_red += 10
                            if row_idx == 6 and position[row_idx + 1][col_idx] != '--': 
                                position_bonus_red += 40
                            else: 
                                if blue_pieces == 1 and red_pieces > 1 :
                                    position_bonus_red += 40
                                if red_pieces == 1 and blue_pieces >= 1:
                                    position_bonus_red -= 40
                        else:
                            position_bonus_red -= 5
                if cell == 'B' : 
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and (position[row_idx - 1][col_idx-1] == 'R' or position[row_idx-1][col_idx+1] == 'R'):
                        position_bonus_blue -= 2
                        if blue_pieces == 1 and red_pieces >= 1 :
                            position_bonus_blue -= 30
                    if row_idx < len(position) -1 and col_idx +1 > 0 and col_idx < len(row) - 2 and ( position[row_idx - 1][col_idx-2] in ['RR', 'BR'] or position[row_idx - 1][col_idx+2] in ['RR', 'BR']): 
                        position_bonus_blue -= 2
                        if blue_pieces == 1 and red_pieces >= 1 :
                            position_bonus_blue -= 30
                    if row_idx < len(position) -2 and col_idx > 0 and col_idx < len(row) - 1 and ( position[row_idx - 2][col_idx-1] in ['RR', 'BR'] or position[row_idx - 2][col_idx+1] in ['RR', 'BR']): 
                        position_bonus_blue -= 2    
                        if blue_pieces == 1 and red_pieces >= 1 :
                            position_bonus_blue -= 30
                    if row_idx < len(position) -1 and row_idx == 1 : 
                        position_bonus_blue += 2
                        if row_idx == 1 and col_idx == 0 and position[row_idx - 1][col_idx + 1] == 'RR' and position[row_idx- 1][col_idx+2] != 'RR' :
                            position_bonus_blue += 50
                        if row_idx == 6 and col_idx == 7 and position[row_idx - 1][col_idx + 1] == 'RR' and position[row_idx-1][col_idx - 2] != 'RR' :
                            position_bonus_blue += 50
                        if row_idx == 1 and col_idx > 0 and col_idx < len(row) - 2 and position[row_idx - 1][col_idx-1] != 'R' and position[row_idx-1][col_idx+1] != 'R' and position[row_idx - 1][col_idx-2] not in ['RR', 'BR']and position[row_idx - 1][col_idx+2] not in ['RR', 'BR']: 
                            position_bonus_blue += 15
                            if row_idx == 1 and position[row_idx - 1][col_idx] == '--': 
                                position_bonus_blue += 50
                            else:
                                if blue_pieces == 1 and red_pieces == 1:
                                    position_bonus_blue += 40
                                if blue_pieces >= 1 and red_pieces == 1:
                                    position_bonus_blue += 40
                                if blue_pieces == 1 and red_pieces >= 1:
                                    position_bonus_blue -= 40   
                        else:
                            position_bonus_blue -= 15
                if cell == 'RR' or cell == 'BR':
                    position_bonus_red += 1
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and (position[row_idx + 1][col_idx-1] == 'B' or position[row_idx+1][col_idx+1] == 'B'): 
                        position_bonus_red -= 1
                        if (red_pieces == 2 and cell == 'RR') or (red_pieces == 1 and cell == 'BR'):
                            position_bonus_red -= 10
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 2 and ( position[row_idx + 1][col_idx-2] in ['RB', 'BB'] or position[row_idx - 1][col_idx+2] in ['BB', 'RB']) :   
                        position_bonus_red -= 1
                        if (red_pieces == 2 and cell == 'RR') or (red_pieces == 1 and cell == 'BR'):
                            position_bonus_red -= 10
                    if row_idx < len(position) -2 and col_idx > 0 and col_idx < len(row) - 1 and  ( position[row_idx + 2][col_idx-1] in ['RB', 'BB'] or position[row_idx - 2][col_idx+1] in ['BB', 'RB']):
                        position_bonus_red -= 1
                        if (red_pieces == 2 and cell == 'RR') or (red_pieces == 1 and cell == 'BR'):
                            position_bonus_red -= 10
                    if row_idx == 6 or row_idx == 5 :      
                        position_bonus_red += 30
                        if row_idx == 6 and col_idx +1 > 0 and col_idx < len(row) - 2 and position[row_idx + 1][col_idx-1] != 'B' and position[row_idx+1][col_idx+1] != 'B' and position[row_idx + 1][col_idx-2] not in ['RB', 'BB'] and position[row_idx + 1][col_idx+2] not in ['RB', 'BB']:    
                            position_bonus_red += 40  
                            if row_idx == 6 and col_idx == 0 and (position[row_idx + 1][col_idx+2] == 'BB' or position[row_idx + 1][col_idx+1] == 'B'):    
                                position_bonus_red -= 5
                            if row_idx == 6 and col_idx == len(row) and (position[row_idx + 1][col_idx-2] == 'BB' or position[row_idx + 1][col_idx -1] == 'B'):    
                                position_bonus_red -= 5            
                        if row_idx == 5 and col_idx + 1 > 0 and col_idx < len(row) - 2 and position[row_idx + 1][col_idx-1] != 'B' and position[row_idx+1][col_idx+1] != 'B' and position[row_idx + 1][col_idx-2] not in ['RB', 'BB'] and position[row_idx + 1][col_idx+2] not in ['RB', 'BB'] and position[row_idx + 2][col_idx-1] not in ['RB', 'BB'] and position[row_idx + 2][col_idx+1] not in ['RB', 'BB']:    
                            position_bonus_red += 40
                            if row_idx == 5 and col_idx == 0 and (position[row_idx + 1][col_idx+2] == 'BB' or position[row_idx + 2][col_idx+1] == 'BB' or position[row_idx + 1][col_idx+1] == 'B'):
                                position_bonus_red -= 5
                            if row_idx == 5 and col_idx == len(row) and (position[row_idx + 1][col_idx-2] == 'BB' or position[row_idx + 2][col_idx-1] == 'BB' or position[row_idx + 1][col_idx-1] == 'B'):
                                position_bonus_red -= 5   
                        else:
                            position_bonus_red -= 1
                if cell == 'BB' or cell == 'RB':
                    position_bonus_blue += 1
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and (position[row_idx - 1][col_idx-1] == 'R' or position[row_idx-1][col_idx+1] == 'R'): 
                        position_bonus_blue -= 2
                        if (blue_pieces == 2 and cell == 'BB') or (blue_pieces == 1 and cell == 'RB'):
                            position_bonus_blue -= 30
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 2 and ( position[row_idx - 1][col_idx-2] in ['RR', 'BR'] or position[row_idx - 1][col_idx+2] in ['RR', 'BR']) :   
                        position_bonus_blue -= 2
                        if (blue_pieces == 2 and cell == 'BB') or (blue_pieces == 1 and cell == 'RB'):
                            position_bonus_blue -= 30
                    if row_idx < len(position) -2 and col_idx > 0 and col_idx < len(row) - 1 and  ( position[row_idx - 2][col_idx-1] in ['RR', 'BR'] or position[row_idx - 2][col_idx+1] in ['RR', 'BR']):
                        position_bonus_blue -= 2
                        if (blue_pieces == 2 and cell == 'BB') or (blue_pieces == 1 and cell == 'RB'):
                            position_bonus_blue -= 30

                    if row_idx == 1 or row_idx == 2 :      
                        position_bonus_blue += 1
                        if row_idx == 1 and col_idx + 1 > 0 and col_idx < len(row) - 2 and position[row_idx - 1][col_idx-1] != 'R' and position[row_idx-1][col_idx+1] != 'R' and position[row_idx - 1][col_idx-2] not in ['RR', 'BR'] and position[row_idx - 1][col_idx+2] not in ['RR', 'BR']:    
                            position_bonus_blue += 40
                            if row_idx == 1 and col_idx == 0 and (position[row_idx - 1][col_idx+2] == 'RR' or position[row_idx - 1][col_idx+1] == 'R'):    
                                position_bonus_blue -= 60
                            if row_idx == 1 and col_idx == len(row) and (position[row_idx - 1][col_idx-2] == 'RR' or position[row_idx + 1][col_idx -1] == 'R'):    
                                position_bonus_blue -= 60  
                        if row_idx == 2 and col_idx + 1 > 0 and col_idx < len(row) - 2 and position[row_idx - 1][col_idx-1] != 'R' and position[row_idx-1][col_idx+1] != 'R' and position[row_idx - 1][col_idx-2] not in ['RR', 'BR'] and position[row_idx - 1][col_idx+2] not in ['RR', 'BR'] and position[row_idx - 2][col_idx-1] not in ['RR', 'BR'] and position[row_idx - 2][col_idx+1] not in ['RR', 'BR']:    
                            position_bonus_blue += 40 
                            if row_idx == 2 and col_idx == 0 and (position[row_idx - 1][col_idx+2] == 'RR' or position[row_idx - 2][col_idx+1] == 'RR' or position[row_idx - 1][col_idx+1] == 'R'):  
                                position_bonus_blue -= 60  
                            if row_idx == 2 and col_idx == len(row) and (position[row_idx - 1][col_idx-2] == 'RR' or position[row_idx - 2][col_idx-1] == 'RR' or position[row_idx - 1][col_idx-1] == 'R'):  
                                position_bonus_blue -= 60    
                        else:
                            position_bonus_blue -= 20
            
            if next == 'blue' : 
                if cell == 'R' :
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and (position[row_idx + 1][col_idx-1] == 'B' or position[row_idx+1][col_idx+1] == 'B'): 
                        position_bonus_red -= 2
                        if red_pieces == 1 and blue_pieces >= 1:
                            position_bonus_red -= 30
                    if row_idx < len(position) -1 and col_idx + 1> 0 and col_idx < len(row) - 2 and(position[row_idx + 1][col_idx-2] in ['RB', 'BB'] or position[row_idx + 1][col_idx+2] in ['RB', 'BB']):
                        position_bonus_red -= 2
                        if red_pieces == 1 and blue_pieces >= 1:
                            position_bonus_red -= 30
                    if row_idx < len(position) -2 and col_idx > 0 and col_idx < len(row) - 1 and(position[row_idx + 2][col_idx-1] in ['RB', 'BB'] or position[row_idx + 2][col_idx +1] in ['RB', 'BB']):
                        position_bonus_red -= 2   
                        if red_pieces == 1 and blue_pieces >= 1:
                            position_bonus_red -= 30
                    if row_idx < len(position) -1 and row_idx == 6 : 
                        position_bonus_red += 2
                        if row_idx == 6 and col_idx == 0 and position[row_idx + 1][col_idx + 1] == 'BB' and position[row_idx+1][col_idx+2] != 'BB' :
                            position_bonus_red += 50
                        if row_idx == 6 and col_idx == 7 and position[row_idx + 1][col_idx - 1] == 'BB' and position[row_idx+1][col_idx - 2] != 'BB' :
                            position_bonus_red += 50
                        if row_idx == 6 and col_idx + 2 > 0 and col_idx < len(row) - 2 and position[row_idx + 1][col_idx-1] != 'B' and position[row_idx+1][col_idx+1] != 'B' and position[row_idx + 1][col_idx-2] not in ['RB', 'BB'] and position[row_idx + 1][col_idx+2] not in ['RB', 'BB']: 
                            position_bonus_red += 15
                            if row_idx == 6 and position[row_idx + 1][col_idx] == '--': 
                                position_bonus_red += 50
                            else: 
                                if blue_pieces == 1 and red_pieces == 1:
                                    position_bonus_red += 40
                                if red_pieces == 1 and blue_pieces > 1:
                                    position_bonus_red -= 40
                                if red_pieces >= 1 and blue_pieces == 1:
                                    position_bonus_red += 40  
                        else:
                            position_bonus_red -= 10
                if cell == 'B' : 
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and (position[row_idx - 1][col_idx-1] == 'R' or position[row_idx-1][col_idx+1] == 'R'):
                        position_bonus_blue -= 1
                        if blue_pieces == 1 and red_pieces > 1 :
                            position_bonus_blue -= 10
                    if row_idx < len(position) -1 and col_idx +1 > 0 and col_idx < len(row) - 2 and ( position[row_idx - 1][col_idx-2] in ['RR', 'BR'] or position[row_idx - 1][col_idx+2] in ['RR', 'BR']): 
                        position_bonus_blue -= 1
                        if blue_pieces == 1 and red_pieces > 1 :
                            position_bonus_blue -= 10
                    if row_idx < len(position) -2 and col_idx > 0 and col_idx < len(row) - 1 and ( position[row_idx - 2][col_idx-1] in ['RR', 'BR'] or position[row_idx - 2][col_idx+1] in ['RR', 'BR']): 
                        position_bonus_blue -= 1    
                        if blue_pieces == 1 and red_pieces > 1 :
                            position_bonus_blue -= 10
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and red_pieces == 1 and blue_pieces == 1 and position[row_idx - 1][col_idx] == 'R':
                        position_bonus_blue -= 50
                    if row_idx < len(position) -1 and row_idx == 1 : 
                        position_bonus_blue += 2
                        if row_idx == 1 and col_idx == 6 and position[row_idx - 1][col_idx] == '--' and position[row_idx-1][col_idx-1] != 'R' and position[row_idx - 1][col_idx-2] != 'RR' : 
                            position_bonus_blue += 50    
                        if row_idx == 1 and col_idx > 0 and col_idx < len(row) - 2 and position[row_idx - 1][col_idx-1] != 'R' and position[row_idx-1][col_idx+1] != 'R' and position[row_idx - 1][col_idx-2] not in ['RR', 'BR']and position[row_idx - 1][col_idx+2] not in ['RR', 'BR']: 
                            position_bonus_blue += 10
                            if row_idx == 1 and position[row_idx - 1][col_idx] == '--': 
                                position_bonus_blue += 50
                            else:
                                if (red_pieces == 1 or red_pieces >= 1)  and blue_pieces == 1:
                                    position_bonus_blue -= 40
                                if blue_pieces > 1 and red_pieces == 1 : 
                                    position_bonus_blue += 40    
                        else:
                            position_bonus_blue -= 5
                if cell == 'RR' or cell == 'BR':
                    position_bonus_red += 1
                    
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and (position[row_idx + 1][col_idx-1] == 'B' or position[row_idx+1][col_idx+1] == 'B'): 
                        position_bonus_red -= 2
                        if (red_pieces == 2 and cell == 'RR') or (red_pieces == 1 and cell == 'BR'):
                            position_bonus_red -= 30
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 2 and ( position[row_idx + 1][col_idx-2] in ['RB', 'BB'] or position[row_idx - 1][col_idx+2] in ['BB', 'RB']) :   
                        position_bonus_red -= 2
                        if (red_pieces == 2 and cell == 'RR') or (red_pieces == 1 and cell == 'BR'):
                            position_bonus_red -= 30
                    if row_idx < len(position) -2 and col_idx > 0 and col_idx < len(row) - 1 and  ( position[row_idx + 2][col_idx-1] in ['RB', 'BB'] or position[row_idx - 2][col_idx+1] in ['BB', 'RB']):
                        position_bonus_red -= 2
                        if (red_pieces == 2 and cell == 'RR') or (red_pieces == 1 and cell == 'BR'):
                            position_bonus_red -= 30
                    if row_idx == 6 or row_idx == 5 :      
                        position_bonus_red += 1
                        if row_idx == 6 and col_idx == 0 and position[row_idx + 1][col_idx+1] != 'B' and position[row_idx + 1][col_idx+2] not in ['RB', 'BB']:  
                            position_bonus_blue += 40  
                        if row_idx == 6 and col_idx == 7 and position[row_idx + 1][col_idx-1] != 'B' and position[row_idx + 1][col_idx-2] not in ['RB', 'BB']:  
                            position_bonus_blue += 40    
                        if row_idx == 6 and col_idx +1 > 0 and col_idx < len(row) - 2 and position[row_idx + 1][col_idx-1] != 'B' and position[row_idx+1][col_idx+1] != 'B' and position[row_idx + 1][col_idx-2] not in ['RB', 'BB'] and position[row_idx + 1][col_idx+2] not in ['RB', 'BB']:    
                            position_bonus_red += 40  
                            if row_idx == 6 and col_idx == 0 and (position[row_idx + 1][col_idx+2] == 'BB' or position[row_idx + 1][col_idx+1] == 'B'):    
                                position_bonus_red -= 60
                            if row_idx == 6 and col_idx == len(row) and (position[row_idx + 1][col_idx-2] == 'BB' or position[row_idx + 1][col_idx -1] == 'B'):    
                                position_bonus_red -= 60            
                        if row_idx == 5 and col_idx + 1 > 0 and col_idx < len(row) - 2 and position[row_idx + 1][col_idx-1] != 'B' and position[row_idx+1][col_idx+1] != 'B' and position[row_idx + 1][col_idx-2] not in ['RB', 'BB'] and position[row_idx + 1][col_idx+2] not in ['RB', 'BB'] and position[row_idx + 2][col_idx-1] not in ['RB', 'BB'] and position[row_idx + 2][col_idx+1] not in ['RB', 'BB']:    
                            position_bonus_red += 40
                            if row_idx == 5 and col_idx == 0 and (position[row_idx + 1][col_idx+2] == 'BB' or position[row_idx + 2][col_idx+1] == 'BB' or position[row_idx + 1][col_idx+1] == 'B'):
                                position_bonus_red -= 60
                            if row_idx == 5 and col_idx == len(row) and (position[row_idx + 1][col_idx-2] == 'BB' or position[row_idx + 2][col_idx-1] == 'BB' or position[row_idx + 1][col_idx-1] == 'B'):
                                position_bonus_red -= 60   
                        else:
                            position_bonus_red -= 20
                if cell == 'BB' or cell == 'RB':
                    position_bonus_blue += 1
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 1 and (position[row_idx - 1][col_idx-1] == 'R' or position[row_idx-1][col_idx+1] == 'R'): 
                        position_bonus_blue -= 1
                        if (blue_pieces == 2 and cell == 'BB') or (blue_pieces == 1 and cell == 'RB'):
                            position_bonus_blue -= 10
                    if row_idx < len(position) -1 and col_idx > 0 and col_idx < len(row) - 2 and ( position[row_idx - 1][col_idx-2] in ['RR', 'BR'] or position[row_idx - 1][col_idx+2] in ['RR', 'BR']) :   
                        position_bonus_blue -= 1
                        if (blue_pieces == 2 and cell == 'BB') or (blue_pieces == 1 and cell == 'RB'):
                            position_bonus_blue -= 10
                    if row_idx < len(position) -2 and col_idx > 0 and col_idx < len(row) - 1 and  ( position[row_idx - 2][col_idx-1] in ['RR', 'BR'] or position[row_idx - 2][col_idx+1] in ['RR', 'BR']):
                        position_bonus_blue -= 1
                        if (blue_pieces == 2 and cell == 'BB') or (blue_pieces == 1 and cell == 'RB'):
                            position_bonus_blue -= 10

                    if row_idx == 1 or row_idx == 2 :      
                        position_bonus_blue += 30
                        if row_idx == 1 and col_idx + 1 > 0 and col_idx < len(row) - 2 and position[row_idx - 1][col_idx-1] != 'R' and position[row_idx-1][col_idx+1] != 'R' and position[row_idx - 1][col_idx-2] not in ['RR', 'BR'] and position[row_idx - 1][col_idx+2] not in ['RR', 'BR']:    
                            position_bonus_blue += 40
                            if row_idx == 1 and col_idx == 0 and (position[row_idx - 1][col_idx+2] == 'RR' or position[row_idx - 1][col_idx+1] == 'R'):    
                                position_bonus_blue -= 5
                            if row_idx == 1 and col_idx == len(row) and (position[row_idx - 1][col_idx-2] == 'RR' or position[row_idx + 1][col_idx -1] == 'R'):    
                                position_bonus_blue -= 5  
                        if row_idx == 2 and col_idx + 1 > 0 and col_idx < len(row) - 2 and position[row_idx - 1][col_idx-1] != 'R' and position[row_idx-1][col_idx+1] != 'R' and position[row_idx - 1][col_idx-2] not in ['RR', 'BR'] and position[row_idx - 1][col_idx+2] not in ['RR', 'BR'] and position[row_idx - 2][col_idx-1] not in ['RR', 'BR'] and position[row_idx - 2][col_idx+1] not in ['RR', 'BR']:    
                            position_bonus_blue += 30 
                            if row_idx == 2 and col_idx == 0 and (position[row_idx - 1][col_idx+2] == 'RR' or position[row_idx - 2][col_idx+1] == 'RR' or position[row_idx - 1][col_idx+1] == 'R'):  
                                position_bonus_blue -= 5  
                            if row_idx == 2 and col_idx == len(row) and (position[row_idx - 1][col_idx-2] == 'RR' or position[row_idx - 2][col_idx-1] == 'RR' or position[row_idx - 1][col_idx-1] == 'R'):  
                                position_bonus_blue -= 5    
                        else:
                            position_bonus_blue -= 1                
   

    #Die Punkte dem Spieler & Gegner zuteilen
    position_bonus_player = 0
    position_bonus_opponent = 0
    if color == 'red' :
        player_pieces = red_pieces
        opponent_pieces = blue_pieces
        position_bonus_player = position_bonus_red
        position_bonus_opponent = position_bonus_blue
        
    if color == 'blue' :
        player_pieces = blue_pieces
        opponent_pieces = red_pieces
        
        position_bonus_player = position_bonus_blue
        position_bonus_opponent = position_bonus_red
                        
    #print((player_pieces - opponent_pieces) + (position_bonus_player - position_bonus_opponent))
    
    return (player_pieces - opponent_pieces) + (position_bonus_player - position_bonus_opponent)
