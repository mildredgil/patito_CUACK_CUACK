Before running the program you must execute the following pip command
pip install -r requirements.txt
this will install all the required dependencies for the compiler to run.

The first part of every pcc program is the same you must declare a program name:

programa Program;
This really does nothing but it is a requirement to start the program.

The second part of any PCC program is the global variables declaration.
We use 3 different kinds of variables: Integers (ent), floating point numbers (deci) and characters (letra). All of these can be made into single or multi level arrays. Be careful to NOT assign values at this part of these programs.
The first thing you declare is the keyword var then the type and after that as many variables of the type as you want. If you need to change types you can just end the statement with its respective ; and declare a new type of variable you want to create.

programa Program;
var ent x,y[4], z[7][8]; 
    deci a;

Afterwards you have the option of adding functions.Functions execute code in another part of the program they can return a value if you wish. Functions can have their own variables declared the same as global variables. Note that you can only call a function that has already been declared beforehand.

Functions are declared as such:
keyword funcion [type] [name]([vars])
[temporal variable declaration] 
{
  [code]
}

programa Program;
var ent x,y[4], z[7][8]; 
    deci xx;

funcion ent suma(ent a, ent b)
ent c
{

}

After declaring all the functions you can declare the main program the same as any other function except it has the name principal and cannot  receive any arguments.
If the function has a return value it must use the command function regresar() to return that value. It only accepts one value and returns that value to the owner of this

funcion ent suma(ent a, ent b)
ent c
{
  regreso(a);
}

To call a function pcc uses the regresa() function. Only need its name and to declare you are going to use it in main.

programa Program;
var ent x,y[4], z[7][8]; 
    deci xx;

funcion ent suma(ent a, ent b)
ent c
{
 regresa(a+b);
}

principal(){
  x= suma(a[1],z[7][8])
}

PCC can print strings, characters and numbers to the screen with function escribe(). Escribe will write on the same line as much as in can and will end the line when the text is finished. Escribe also takes an unlimited amount of both variable and strings if they are separated by commas and will print them in the order they were sent.

programa Program;
var ent x,y[4], z[7][8]; 
    deci xx;

principal(){
  escribe(“hello ”,” word ”, “1”);
}

PCC can receive data to be saved onto a variable using the command lee(). It only takes one variable and asked for input to the user.
programa Program;

var  ent x,y[4], z[7][8]; 

principal(){
  escribe(“Write a number”);
  lee(x);
escribe(“hello ”, ” word ”, x);
}

PCC can also assign values to variables like so:
a=1;
PCC can also solve basic math operations while assigning values.
a=4*3/2+1;
 
PCC can do comparisons between both variables and constants using the si command like so. If the expression is true PCC will run the block of code inside its brackets if not it will just ignore it.
 si (a==b) {
      escribe(a);
    }
You can also add a sino command after si that will only happen if si is not triggered.
si (a<b) {
escribe(a);
} sino {
escribe(b);
}

PPC has 2 types of loops for loops and while loops called desde y mientras respectively.
The while loop mientras has the following structure:
mientras([condition]) haz {
	[code]
}
a=0;
mientras(a<5) haz {
	escribe(a);
a=a+1;
}
while the condition is true the code will keep running itself. the condition is check after the whole block of code is done.
The for loop has the following structure:
desde [initialize ent variable] hasta [integer number] hacer {
  [code]
}

desde a=0 hasta 5 hacer {
  escribe(a);
}
At the end of the code block the initialized variable is increased by one, checks if the initialized variable is equal to the integer number and if so repeats loop. 
NOTE: on both these loops there is an initial check before the code is rune if the condition is true the loop does not run.


----
TODO: 
    Multiplicacione de matrices: ultima dimension = primera dimension