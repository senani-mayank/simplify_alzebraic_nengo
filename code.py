#only X and Y

import nengo
import numpy as np

model = nengo.Network()
xcount = 0
ycount = 0
x_flag = True
y_flag = True



def incr_xcount(  ):
    global xcount
    global x_flag
    x_flag = False
    xcount = xcount + 1
def incr_ycount(  ):
    global ycount
    ycount = ycount + 1
    
def set_flag( vari, val ) :
    if( vari == "x" ):
        global x_flag  
        x_flag = val
    elif( vari == "y" ):
        global y_flag  
        y_flag = val    
   
#variables
prev_count_direction = 'd'
prev_append_dir = 'd'
count = 0
expression = ''
append_flag = False
var = ''

#set_var( char )
def set_var( v ) :
    global var
    var = v

def reset_count() :
    global count
    count = 0
  
#incr_count( int )
def incr_count( value, direction ) :
    global prev_count_direction
    if( prev_count_direction != direction ) :
        global count
        count = count + value
        prev_count_direction = direction
    
#evaluate()
def evaluate() :
    global expression
    final_expression = ''
    var_map = dict()
    i = 0
    while i < len(expression) :
        sign = expression[i]
        value = int(expression[i + 1])
        variable = expression[ i + 2]
        
        if sign == '-' :
            value = -value
        
        if not (variable in var_map) :
            var_map[ variable ] = 0
            
        var_map[ variable ] = var_map[ variable ] + value
        i = i + 3
    
    for key in var_map :
        final_expression = final_expression + ('+' if value >= 0 else '')  + str(var_map[key]) + key
    print(expression)
    return final_expression
    
#append to current expression
def append_to_expr( direction ) :
    global prev_append_dir
    global expression

    if direction == prev_append_dir :
        return expression
    global var
    global count
    global append_flag
    expression = expression + '+'
    expression = expression + str(count) + var
    prev_append_dir = direction
    reset_count(  )

    return expression

with model:
            



   # Example 3: a two-joint arm    
    def arm_function(t, angles):
        
        ivar = angles[0]
        icount = angles[1]
        itrig = angles[2]
        html = ''
        
        if (ivar >=0.8) and (ivar<=1.0) :
            set_var( 'X' )
        elif (ivar >= -1.0) and (ivar<= -0.8) :
            set_var( 'Y' )
            
        if (icount >= 0.8 and icount <= 1.0 ) :
            incr_count( 1, 'u' )
        elif ( icount>= -1.0 and icount <= -0.8 ) :
            incr_count(1, 'd')
        
        if itrig >= 0.8 and itrig <= 1.0 :
            #evaulate expression
            append_to_expr('u')
        elif itrig >= -1.0 and itrig <= -0.8 :
             append_to_expr('d')
       # if html == '' : 
        #    html = '<h3> ivar = ' + str(ivar) + ' icount = ' + str(icount) + ' itrig = ' + str(itrig) + '</h3>'
        
        html = html + '</br>' + '<h3>Expression = ' + expression + '</h3>'
        html = html + '</br>' + '<h3>Final Expression = ' + evaluate() + '</h3>'
        html = html + '</br>' + '<h3>Var = ' + var + '</h3>'
        html = html + '</br>' + '<h3>Count = ' + str(count) + '</h3>'
        arm_function._nengo_html_ = html
        
    stim_angles = nengo.Node([0.0, 0.0, 0.0])
    angles = nengo.Ensemble(n_neurons=1500, dimensions=3)
    arm = nengo.Node(arm_function, size_in=3)
    nengo.Connection(stim_angles, angles)
    nengo.Connection(angles, arm)
    