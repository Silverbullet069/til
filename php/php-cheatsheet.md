# PHP Cheatsheet

<!-- tl;dr starts -->

My father's website is written in old PHP version, despite I'm a JavaScript/TypeScript and Python guy, I need to learn PHP.

<!-- tl;dr ends -->

## Coding convention

- Use camelCase for variable naming, snake_case for function naming.
- Turn off warnings and errors on production, to not give hackers any clue, even if something goes wrong. Save them in an error logger.
- There are 4 ways to use variables in `echo`:

  - Variable interpolation, with curly braces. High readablity. Doesn't allow function call.

  ```php
  echo "Welcome, {$name}!";
  ```

  - String concatenation. Flexible, low readability. Allow function call.

  ```php
  echo "Welcome, " . $name . "!";
  ```

  - Parameter separation (only worked with `echo`). More optimized (but subtle)

  ```php
  echo "Welcome, ", $name, "!";
  ```

  - String formatter (since PHP4):

  ```php
  $format = "Welcome, %s!";
  echo sprintf($format, $name);
  ```

## From my Playground

```php
<?php
// NOTE: declare() must be THE FIRST statement in the file
declare(strict_types=1);
?>

<?php
// this is a comment
# this is also a comment
/* this is a multi-line
comment */

# Add a text node to HTML
echo "Hello, World!"; // DO NOT FORGET SEMICOLON!

# Variable declaration
$x;                   // its value if not specified, will be assigned automatically to NULL
$x = 1;               // with value

# Multiple variables assignment
$x = $y = $z = 1;

# Arithmetic operation
$x = 1;               // integer
$y = 6969;            // integer
$z = "Hello, World";  // string
echo $x + $y;         // 6970
echo $x + $z;         // Uncaught TypeError: Unsupported operand types: int + string...

/**
 * Data Type
 *
 * There are 8 different data type:
 * - NULL: valueless variables are assigned with NULL when created.
 * - Boolean
 * - String
 * - Integer
 * - Float
 * - Array
 * - Object: new Class()
 * - Resource
 *
 * Additional data types for numbers:
 * - Infinity
 * - NaN
 *
 * PHP is a _loosely typed language_. The variable's type is based on its value.
 * NOTE: In PHP 7, type declaration were added, allowing developers to add explicit data type when declaring a function.
 */

var_dump(null);         // null
var_dump(true);         // bool(true)

/**
 * String
 */
var_dump('John Doe');   // string(8) "John Doe"
var_dump("John Doe");   // string(8) "John Doe"

$x = "Doe";
echo 'John $x';         // John $x    // No variable interpolation
echo "John $x";         // John Doe   // Variable interpolation

# Built-in functions for string
echo strlen("John Doe");          // length: 8
echo str_word_count("John Doe");  // count words: 2
echo strpos("John Doe", "Doe");   // position: 5
echo strtoupper("John Doe");      // uppercase: JOHN DOE
$x = "John Doe";
echo str_replace("John", "Jane", $x); // replace: Jane Doe
echo strrev("Hello World");       // reverse: dlroW olleH
echo trim("  John Doe   ");       // trim: John Doe
$y = explode(" ", $x);            // the 1st argument acts as the separator
print_r($y)                       // Array ( [0] => John [1] => Doe )
// NOTE: to display array, you must use print_r function
echo substr($x, 5, 2);            // slice: Do
echo substr($x, 5);               // slice to the end: Doe
echo substr($x, -3);              // slice from the end: Doe
echo substr($x, -3, 2);           // Do
echo substr($x, 2, -1);           // negative length: hn Do

# String concatenation
# Instead of using plus operator, PHP use dot operator
$x = "Hello";
$y = "World";
$z = $x . $y;
echo $z; // HelloWorld
$z = $x . " " . $y;
echo $z; // Hello World
$z = "$x $y";
echo $z; // Hello World

# String escape character
$x = "For now we will call him \"John Doe\".";
echo $x;

/**
 * Integers
 * - Ranged from -2^31 to 2^31 - 1 (32-bit system), -2^63 to 2^63 - 1 (64-bit system). A value exceed that ranged will be stored as Float.
 * - Can be specified in decimal (base 10), hexadecimal (base 16), octal (base 8), or binary (base 2).
 */
var_dump(1);            // int(1)
echo PHP_INT_MAX;       // the largest integer supported: 9223372036854775807
echo PHP_INT_MIN;       // the smallest integer supported: -9223372036854775808
echo is_int(1);         // 1 (NOTE: the output is boolean)
echo var_dump(is_int(1));    // bool(true)
echo var_dump(is_int(1.0));  // bool(false)
echo is_integer(1);     // alias of is_int()
echo is_long(1);        // alias of is_long()

/**
 * Floats
 *
 * Commonly store a value from 2.2250738585072E-308 to 1.7976931348623E+308 (64-bit)
 * Maximum precision of 14 digits
 */
var_dump(3.14);                 // float(3.14)
echo PHP_FLOAT_MAX, "<br/>";    // 1.7976931348623E+308
echo PHP_FLOAT_MIN, "<br/>";    // 2.2250738585072E-308
echo PHP_FLOAT_DIG, "<br/>";    // The number of decimal digits that can be rounded into a float and back WITHOUT PRECISION LOSS 15
var_dump(is_float(1.0));        // bool(true)

/**
 * Infinity
 * Any number that is larger than PHP_FLOAT_MAX is considered infinite
 */
$x = 1.9e400;
var_dump($x);           // float(INF)

/**
 * NaN (Not a Number)
 * Used for impossible methematical operations, often results in imaginary number
 */
$x = sqrt(-1);
$y = acos(8);
var_dump($x);           // float(NaN)
var_dump($y);           // float(NaN)

/**
 * Numerical Strings
 * NOTE: From PHP7.0, hexadecimal strings (i.e. "0xf4c3b00c") aren't considered numerical strings.
 */
$x = "6969";
$hex = "0xf4c3b00c";
var_dump($x);               // string(4) "6969"
var_dump(is_int($x));       // bool(false)
var_dump(is_numeric($x));   // bool(true)
var_dump(is_numeric($hex)); // bool(false)

/**
 * Type Casting
 *
 * There are 7 different statements:
 * - (int)
 * - (string)
 * - (float)
 * - (bool)
 * - (array)
 * - (object)
 * - (unset): converts to NULL
 */
$x = 1.2;
$y = "1.7";
$float_to_int = (int)$x;
$str_to_int = (int)$y;
echo "Cast float to int: $float_to_int";
echo "Case str to int: $str_to_int";

$int_to_str = (string) $x;
$float_to_str = (string) $y;
var_dump($int_to_str);
var_dump($float_to_str);

class Car {
  public $color;
  public $model;
  public function __construct($color, $model) {
    $this->color = $color;
    $this->model = $model;
  }
  public function printMessage() {
    return "My car is a $this->color $this->model!";
  }
}
$myCar = new Car("Black", "Toyota");
var_dump($myCar); // object(Car)#1 (2) { ["color"]=> string(5) "Black" ["model"]=> string(6) "Toyota" }

# Change data type
$x = 5;
var_dump($x);
$x = "abc";
var_dump($x);

/**
 * Variable scopes: global, local, static.
 */

# Global - variables declare outsite a function.

# Accessible directly at script-level, not only in the file where it gets declared but in other files as well if they `include()` this file.

# Not accessible at function-level or block-level, unlike other languages who allow variable shadowing, you can have local variables with the same name in different functions and outside functions as well.

# To access it at function-level, `global` keyword or `$GLOBALS[<var_name>]` must be used

# However, there are some drawbacks when using global variables like this
# - Hidden dependencies between files are untrackable, hard to maintain.
# - Create unexpected behavior when code in one place is changed and affects code elsewhere.
# - Name conflicts, accidental overwriting.
# - Hard to isolate components for unit testing.

# Alternatives (more about this later):
# 1. Dependency Injection
# 2. Classes and Objects
# 3. Use constants for unchanged global values

$x = 5;
function test() {
  echo "<p>Variable x inside function test() is: $x</p>"; // nothing
}
function test2() {
  # Local - variables declare within a function
  $x = 5;
  echo "<p>Variable x inside function test2() is: $x</p>"; // 5
}
function testGlobal() {
  global $x;
  echo "Global x: $x";
}
test();
test2();
testGlobal();
echo "<p>Variable x outside function test() is: $x</p>"; // 5
echo "<p>Variable y after calling function testGlobal() is: $y</p>"; // 11

// GLOBALS[<index>] array
$z = 1;
$GLOBALS['z'] = $GLOBALS['x'] + $GLOBALS['z'];
echo "<p>Variable z: $z</p>"; // Output: 6

# static - Local variables that won't be deleted after functions finished their execution.
function testStatic() {
  static $x = 0;
  echo "<p>Static x: $x</p>";
  $x++;
}
testStatic();
testStatic();
testStatic();

/**
 * Two statements used to output: `echo` and `print`.
 *
 * | Criteria              | `echo`          | `print`                          |
 * | --------------------- | --------------- | -------------------------------- |
 * | **Return value**      | none            | `1` (can be used in expressions) |
 * | **No. of arguments** | multiple (rare) | ONE, and only ONE                |
 * | **Speed**             | Faster          | Slower                           |
 */
echo("echo with parenthesis!");
echo "echo without parenthesis!";
echo "Hello", " World!"; // DO NOT FORGET THE COMMA
echo "This ", "string ", "was ", "made ", "with multiple parameters.";
$txt1 = "Hello";
$txt2 = "World";
echo "<p>$txt1, $txt2</p>";
echo '<p>' .$txt1. ', ' .$txt2. '</p>'; // you must use 2 dot operator

print "print without parenthesis";
print("print with parenthesis"):
// the rest is the same as echo()

/**
 * Math
 */
echo pi();                // 3.1415926535898
echo min(1, 2, 3, 4, 5);  // 1
echo max(-5, -4, -3);     // -3
echo abs(-5);             // 5
var_dump(sqrt(64));       // float(8)
echo round(0.5);          // 1
echo round(0.4999999);    // 0
var_dump(rand(1, 6));     // int(1|2|3|4|5|6)

/**
 * Constant
 *
 * - A variable whose value can't be changed
 * - Automatically global regardless where it was declared.
 * - Despite being global, a constant can be accessed inside functions.
 * - NOTE: Do not use $ when referring, using $ refers to another variable.
 *
 * There are 2 ways to create constants: `define()` vs `const`:
 * - `const` can't be used inside another block scope, such as if statement or functions
 * - `define()`, however, can be used everywhere.
 */
define("BR", "<br/>");
define("BR", "not <br/>"); // not an error but a warning: Constant BR already defined in [FILE] on line [LINE]
const NAME = "John Doe";
echo NAME, BR;              // John Doe
echo "Hello, " . NAME . BR; // Hello, John Doe
echo sprintf("Hello from sprintf, %s", NAME), BR; // Hello from sprintf, John Doe

# Constant array
define("cars", [
  "Toyota",
  "Bentley",
  "Mercedes",
  "BMW"
]);
echo cars[0];             // Toyota

define("HELLO", "Welcome to PHP School");
function testConstant() {
  echo "This is x: $x";   // nothing
  echo HELLO;             // Welcome to PHP School
}
testConstant();

class Test {
  public function getClassName() {
    return __CLASS__;
  }
  public function getMethod() {
    return __METHOD__;
  }
}

$test = new Test();
echo $test->getClassName();     // Test
echo $test->getMethod();        // Test::getMethod

echo __DIR__, BR;               // /home/silverbullet069/.playground/php
echo __FILE__, BR;              // /home/silverbullet069/.playground/php/index.php
function testPre() {
  echo __FUNCTION__, BR;        // testPre
  echo __LINE__, BR;            // 226
}
testPre();

/**
 * Operators
 *
 * There are 8 operator groups
 * - Arithmetic
 * - Assignment
 * - Comparison
 * - Incremental/Decremental
 * - Logical
 * - String
 * - Array
 * - Conditional assignment (a.k.a ternary)
 */

# Arithmetic
$x = 12;
$y = 5;
echo "x % y = ", $x % $y, var_temp() BR;       // 2
echo "x ** y = ", $x ** $ y, BR;    // 248832

# Assignment
$y = $x;    // y = x
$y += $x;   // y = y + x
$y -= $x;   // y = y - x
$y *= $x;   // y = y * x
$y /= $x;   // y = y / x
$y %= $x;   // y = y % x

# Comparison
// integer vs numerical string
$x = 100;
$y = "100";
var_dump($x == $y);     // bool(true)
var_dump($x === $y);    // bool(false)
var_dump($x <> $y);     // bool(false)
var_dump($x != $y);     // bool(false)
var_dump($x !== $y);    // bool(true)
$y = 101;
var_dump($x <=> $y);    // int(-1)
$y = 99;
var_dump($x <=> $y);    // int(1)
$y = 100;
var_dump($x <=> $y);    // int(0)

# Increment/Decrement
$x = 100; echo ++$x;    // 101, increase $x by one first, then return $x
$x = 100; echo $x++;    // 100, return $x, then increase $x by 1
$x = 100; echo --$x;    // 99, decrease $x by 1, then return $x
$x = 100; echo $x--;    // 100, return $x, then decrease $x by 1

# Logical
var_dump($x and $y);
var_dump($x && $y); // same
var_dump($x or $y);
var_dump($x || $y); // same
var_dump($x xor $y);
var_dump(!$x);

# String
$x = "Hello";
$x .= "World";
echo $x;    // HelloWorld

# Array
$x = array("a" => "red", "b" => "green");
$y = array("c" => "blue", "d" => "yellow");
print_r($x + $y); // Array ( [a] => red [b] => green [c] => blue [d] => yellow )
// NOTE: If you want to print an array, you must use print_r() function

$x = array("a" => "red", "b" => "green");
$y = array("a" => "red", "b" => "green");
var_dump($x == $y);   // true
var_dump($x === $y);  // false, not in the same order
var_dump($x <> $y);   // false
var_dump($x !== $y);  // true

# Conditional assignment
$x = 1;
$y = $x === 1 ? 2 : 0;
echo "y: $y";

// NOTE: the following are type casted to bool(false)
// - Empty string
// - 0 (integer)
// - false
// - NULL

$z = "" ?? 1;
var_dump($z);   // string(0) ""
$z = false ?? 1;
var_dump($z);   // bool(false)
$z = null ?? 1;
var_dump($z);   // int(1)

/**
 * if Statements
 *
 * if...else
 * if...elseif...else
 * switch
 *
 * if Operators, same as above
 */
if (1 < 0) {
  echo "Have a good day!";
} elseif (2 < 1) {
  echo "I'm inside elseif";
} else {
  echo "I'm inside else"; // chosen
}

$x = 1;
switch ($x) {
  // default can be here as well
  default:
    echo "Not zero, one, or two!";
    break; // remember to add
  case 0:
    echo "zero";
    break;
  case 1:
    echo "one"; // chosen!
    break;
  case 2:
    echo "two";
    break;
  // common code blocks
  case 3:
  case 4:
  case 5:
    echo "three, four, five";
    break;
  default:
    echo "Not zero, one, or two!";
}

/**
 * Loops
 *
 * while
 * do..while
 * for
 * foreach
 */

$i = 1;
while ($i < 10) {
  echo $i;
  $i++; // 123456789
}

// second syntax
$i = 1;
while ($i < 10):
  echo $i; // 123456789
  $i++;
endwhile;

for ($x = 0; $x < 10; ++$x) {
  echo "$x"; // 01234567889
}

// indexed array
$colors = array("red", "green", "blue", "purple");

// for each
// Iterate through each element in the array using foreach
// This approach is preferred as it eliminates the need for index variables and array length tracking, providing cleaner, more maintainable code and avoid infinite loop

foreach ($colors as $x) {
  if ($x === "blue") break;
  echo $x, BR; // red, green
}

// associative array
$members = array("Peter" => "35", "Ben" => "27", "Ashley" => "19");

foreach ($members as $x=>$y) {
  if ($x === "Peter") continue;
  echo "$x: $y", BR; // Ben: 27, Ashley: 19
}

class Car {
  public $name;
  public $color;

  public function __construct($name, $color) {
    $this->name = $name;
    $this->color = $color;
  }
}

$myCar = new Car("Toyota", "black");
foreach($myCar as $x => $y) {
  echo "$x: $y", BR;
}

# Foreach Byref
# NOTE: pass-by-reference DOES NOT improve performance, since PHP's engine use CoW (Copy-on-Write) mechanism
$colors = array("red", "green", "blue", "yellow");
foreach ($colors as $x) {
  if ($x === "red") $x = "pink"; // no changed!
}
var_dump($colors); // output: array(4) { [0]=> string(3) "red" [1]=> string(5) "green" [2]=> string(4) "blue" [3]=> string(6) "yellow" }

foreach ($colors as &$x) {
  if ($x === "red") $x = "pink";
}
var_dump($colors); // output array(4) { [0]=> string(3) "red" [1]=> string(5) "green" [2]=> string(4) "blue" [3]=> &string(6) "yellow" }

// NOTE: the ampersand PHP creates a real reference to the last element of $colors array AFTER the loop completed, any manipulation towards $x will affect the final value in $colors array

// To avoid unexpected behavior, unset $x right after foreach
unset($x);

# alternative syntax
foreach ($colors as $x):
  echo $x;
endforeach;

/**
 * Function
 *
 * Over 1000 built-in functions
 * It's best to use AI to know when to use which
 *
 * Functions that developers wrote are called User-defined function
 *
 * NOTE: Function names are case-INsensitive! WTF?
 */

# Number of arguments and default value
function greet($name, $count = 1) {
  for ($i = 0; $i < $count; ++$i)
    echo "Hello, $name!", BR;
}
GREET("John Doe", 3); // Hello, John Doe! x3
greet("Jane Doe");    // Hello, Jane Doe!

# Pass by value
function sum(int $x, int $y) {
  return $x + $y;
}
echo "5 + 10 = " . sum(5, 10), BR; // 5 + 10 = 15
echo sum(5, "5 days"), BR; // 10, which is wrong

# Pass by reference
$x = 1;
function addOne(&$value) {
  $value += 1;
}
addOne($x);
echo "x: $x", BR;

# Variadic function
# Function with unknown number of argument
# Use ... operator
function sum2(...$arr) {
  // $len = count($arr);
  // $sum = 0;
  // for ($i = 0; $i < $len; ++$i)
  //   $sum += $arr[$i];

  $sum = 0;
  foreach ($arr as $x) {
    $sum += $x;
  }
  return $sum;
}

$sum = sum2(1, 2, 3, 4, 5);
echo "Sum: $sum", BR;

# Variadic argument must be the last argument
function familyName($lastName, ...$firstName) {
  $str = "";
  foreach($firstName as $name) {
    $str = $str."Hi, $name $lastName".BR;
  }
  return $str;
}
echo familyName("Doe", "John", "Jane");

# Return type declaration
function addFloat(float $a, float $b): float {
  return $a + $b;
}
echo addFloat(1.2, 3.4);
function addFloat2(float $a, float $b): int {
  return (int)($a + $b);
}
echo addFloat2(1.2, 3.4);

/**
 * Array
 *
 * Special variable that hold many values under a single name
 *
 * There are 3 types of arrays:
 * - Indexed array
 * - Associative array
 * - Multidimensional array
 *
 * Array items can be of any data type.
 * There are a lot of built-in functions for array
 */
var_dump([1, 2, 3]);    // array(3) { [0]=> int(1) [1]=> int(2) [2]=> int(3) }

// Array items can be of any data type.
$myArr = array("Toyota", 5, true, ["John", "Doe"], null);

// Array built-in functions
echo count($myArr);

# Create arrays

// 2 ways
$cars = array("Toyota", "Volvo", "Mercedes");
$cars = ["Toyota", "Volvo", "Mercedes"];

// Trailing comma is allowed
$cars = [
  "Toyota",
  "Volvo",
  "Mercedes",
];

// Array keys for indexed arrays are allowed
$cars = [
  0 => "Toyota",
  1 => "Volvo",
  2 => "Mercedes"
];

// same as keys for associative arrays
$cars = [
  "brand" => "Toyota",
  "model" => "Civic",
  "color" => "Black"
];

// Create empty array
$myArr = [];
// Mixing array keys
$myArr = [];
$myArr[0] = "apple";
$myArr[1] = "banana";
$myArr["fruit"] = "tropical";
print_r($myArr);

# Access array
$brands = ["Toyota", "Volvo", "Mercedes"];
echo $brands[0]; // indexed array

$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969];
echo $cars["year"]; // associative array

// Double or single quotes are good
echo $cars["model"];
echo $cars['model'];

# Update array
$brands = ["Toyota", "Volvo", "Mercedes"];
$brands[0] = "Mazda"; // indexed array

$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969];
$cars["year"] = 1964; // associative array

$cars = array("Volvo", "BMW", "Toyota");
foreach ($cars as &$x) {
  $x = "Ford";
}
$x = "ice cream";
var_dump($cars); // array(3) { [0]=> string(4) "Ford" [1]=> string(4) "Ford" [2]=> &string(9) "ice cream" }

unset($x); // Remember to call unset() when assign item value by reference

# Add array item
$brands = ["Toyota", "Volvo", "Mercedes"]; // indexed array
$brands[] = "BMW";
array_push($brands, "Audi");
array_push($brands, "Chevrolet", "Lexus", "Nissan", "Suzuki");
print_r($brands);
// Array ( [0] => Toyota [1] => Volvo [2] => Mercedes [3] => BMW [4] => Audi [5] => Chevrolet [6] => Lexus [7] => Nissan [8] => Suzuki )

$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969]; // associative array
$cars["owner"] = "JW";
$cars += ["color" => "black", "status" => "broken"];
print_r($cars);
// Array ( [brand] => Ford [model] => Mustang [year] => 1969 [owner] => JW [color] => black [status] => broken )

# Remove Array item
$brands = ["Toyota", "Volvo", "Mercedes"]; // indexed array

// 2nd: where to start, 3rd: how many items
// re-arrange index after remove
array_splice($brands, 1, 1);
print_r($brands); // Array ( [0] => Toyota [1] => Mercedes )

unset($brands[0]);
print_r($brands); // Array ( [1] => Mercedes )

$brands = ["Toyota", "Volvo", "Mercedes"];
array_splice($brands, 1, 2);
print_r($brands); //  Array ( [0] => Toyota )

$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969]; // associative array
unset($cars["brand"], $cars["model"]);
print_r($cars); // Array ( [year] => 1969 )

// Remove based on value, not keys
$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969]; // associative array
$newCars = array_diff($cars, ["Mustang", 1969]);
print_r($newCars); // Array ( [brand] => Ford )

array_shift($brands); // Remove the first item
array_pop($brands);   // Remove the last item

# Sorting
$brands = ["Toyota", "Volvo", "Mercedes"];
$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969];
$mixed = [true, false, null, sqrt(-1), "abc"];
sort($brands);      // indexed, ascending
sort($cars);        // NOTE: when used with with an associative array, its keys are stripped off
sort($mixed);
var_dump($brands);  // array(3) { [0]=> string(8) "Mercedes" [1]=> string(6) "Toyota" [2]=> string(5) "Volvo" }
var_dump($cars);    // array(3) { [0] => int(1969) [1]=> string(4) "Ford" [2]=> string(7) "Mustang" }
var_dump($mixed);   // array(5) { [0] => bool(false) [1]=> NULL [2]=> bool(true) [3]=> string(3) "zzz" [4]=> float(NAN) }

$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969];
rsort($brands);     // indexed, descending
var_dump($brands);  // array(3) { [0]=> string(5) "Volvo" [1]=> string(6) "Toyota" [2]=> string(8) "Mercedes" }

$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969];
asort($cars);       // associative, ascending, value
var_dump($cars);    // array(3) { [0]=> int(1969) [1]=> string(4) "Ford" [2]=> string(7) "Mustang" }

$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969];
arsort($cars);      // associative, descending, value
var_dump($cars);    // array(3) { [2]=> string(7) "Mustang" [1]=> string(4) "Ford" [0]=> int(1969) }

$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969];
ksort($cars);       // associative, ascending, key
var_dump($cars);    // array(3) { ["model"]=> string(7) "Mustang" ["brand"]=> string(4) "Ford" ["year"]=> int(1969) }

$cars = ["brand" => "Ford", "model" => "Mustang", "year" => 1969];
krsort($cars);      // associative, descending, key
var_dump($cars);    // array(3) { ["year"]=> int(1969) ["model"]=> string(7) "Mustang" ["brand"]=> string(4) "Ford" }

# Multidimensional Array
$cars = [
  ["Volvo", 22, 18],
  ["BMW", 15, 13],
  ["Saab", 5, 3],
  ["Land Rover", 17, 15],
];

# Built-in Array function
# IMO, it's impossible to learn all of them. Using AI to find the right function for your problem.

/**
 * Superglobals
 *
 * PHP 4.1.0
 *
 * Built-in variables that are available in all scopes: script-level, function-level, block-level, per-file and across files
 */

# $GLOBALS
$x = 1;
function testSuperglobal() {
  echo "x: " . $GLOBALS['x'], BR;
}
testSuperglobal();

function testGlobalKeyword() {
  global $x;
  echo "x: $x";
}
testGlobalKeyword();

function testCreateGlobalVarInFunction() {
  $GLOBALS["abc"] = "abc";
}
testCreateGlobalVarInFunction();
echo $GLOBALS["abc"];

# $_SERVER
echo "PHP_SELP: ", $_SERVER["PHP_SELF"] ?? "Not set", BR;
echo "SERVER_ADDR: ", $_SERVER["SERVER_ADDR"] ?? "Not set", BR;
echo "SERVER_NAME: ", $_SERVER["SERVER_NAME"] ?? "Not set", BR;
echo "SERVER_SOFTWARE: ", $_SERVER["SERVER_SOFTWARE"] ?? "Not set", BR;
echo "SERVER_PROTOCOL: ", $_SERVER["SERVER_PROTOCOL"] ?? "Not set", BR;
echo "REQUEST_METHOD: ", $_SERVER["REQUEST_METHOD"] ?? "Not set", BR;
echo "REQUEST_TIME: ", $_SERVER["REQUEST_TIME"] ?? "Not set", BR;
echo "HTTP_HOST: ", $_SERVER["HTTP_HOST"] ?? "Not set", BR;
echo "HTTP_REFERER: ", $_SERVER["HTTP_REFERER"] ?? "Not set", BR;
echo "HTTPS: ", $_SERVER["HTTPS"] ?? "Not set", BR;
echo "REMOTE_ADDR: ", $_SERVER["REMOTE_ADDR"] ?? "Not set", BR;
echo "REMOTE_HOST: ", $_SERVER["REMOTE_HOST"] ?? "Not set", BR;
echo "REMOTE_PORT: ", $_SERVER["REMOTE_PORT"] ?? "Not set", BR;
echo "SCRIPT_FILENAME: ", $_SERVER["SCRIPT_FILENAME"] ?? "Not set", BR;
echo "SERVER_ADMIN: ", $_SERVER["SERVER_ADMIN"] ?? "Not set", BR;
echo "SERVER_PORT: ", $_SERVER["SERVER_PORT"] ?? "Not set", BR;
echo "SERVER_SIGNATURE: ", $_SERVER["SERVER_SIGNATURE"] ?? "Not set", BR;
echo "PATH_TRANSLATED: ", $_SERVER["PATH_TRANSLATED"] ?? "Not set", BR;
echo "SCRIPT_NAME: ", $_SERVER["SCRIPT_NAME"] ?? "Not set", BR;
echo "SCRIPT_URI: ", $_SERVER["SCRIPT_URI"] ?? "Not set", BR;

/**
 * Regular expression
 *
 * Modifiers:
 * - i (case-insensitive)
 * - m (multiline search)
 * - u (enables correct matching of UTF-8 encoded patterns)
 */

$str = "John Doe";
$pattern = "|John|i";
echo preg_match($pattern, $str);  // 1

$str = "The rain in SPAIN falls mainly on the plains.";
$pattern = "|ain|i";
echo preg_match_all($pattern, $str); // 4
echo preg_replace($pattern, "abc", $str);  // The rabc in SPabc falls mabcly on the plabcs.

/**
 * Validation and sanitization
 * Validation = determine if the data is in correct form.
 * Sanitization = remove any illegal characters from the data.
 *
 * Website, in production, to ensure data integrity and security when handling
 * external input/data, enforces client-side and server-side validation and
 * sanitization.
 *
 * BOTH client and server need to implement this behavior since the client-side
 * protection can be easily bypassed if the requests are sent directly to server
 * without browsers by using tools such as wget, curl, Postman, ...
 *
 * Best practice:
 * - Validation's mandatory every time, but sanitization iso't.
 * - Always save data as is, always escape data when outputting. This applies to
 * ANY data, not just for external input.
 * - Validation should follow business rules not related to security. That is
 * sanitization's job.
 * - Sanitization = anti-pattern. It's a special and explicitly "filter" that
 * converts invalid data into valid data. In other way, it's a destructive
 * process, it renders any subsequent tasks that requires data originality
 * impossible.
 * - DO NOT store sanitized input. It means the system is blindly modifying user
 * input and implies that the system can now safely execute user data in any
 * context.
 * - Popular frameworks (e.g. Laravel, Symfony) have baked-in validator. If you
 * are using raw PHP, best option is to take a PSR compatible validation library
 * (a Symfony validator, ...)
 *
 * SANITIZE ALL user supplied data in these places:
 * - CLI process prompts.
 * - Database queries.
 * - Email (make sure it's not passing extra headers nor using your system as an
 * email spam relay)
 * - HTML Web Page (e.g. CMS, comment system, ...)
 *
 * List of external input/data:
 * - URL.
 * - Form.
 * - Cookies.
 * - File uploads
 * NOTE: In general, HTTP Request Headers and HTTP Request Body
 * - Web services data
 * - Server variables
 * Read OWASP list to know which is Top 10 vulnerabilities and how to mitigate
 * them in PHP.
 */

function sanitize($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}

$fname = $lname = $email = $gender = $comment = $website = "";
$fnameErr = $lnameErr = $emailErr = $genderErr = $commentErr = $websiteErr = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  if (empty($_POST["fname"])) {
    $fnameErr = "First name is required.";
  } else {
    $fname = sanitize($_POST["fname"]); // same as $_REQUEST["fname"]
    # 2 - preg_match()
    if (!preg_match("/^[a-zA-Z-' ]*$/", $fname)) {
      $fnameErr = "Only letters, dashes, apostrophes and whitespace are allowed!";
    }
  }

  if (empty($_POST["lname"])) {
    $lnameErr = "Last name is required.";
  } else {
    $lname = sanitize($_POST["lname"]); // same as $_REQUEST["lname"]
    if (!preg_match("/^[a-zA-Z-' ]*$/", $lname)) {
      $lnameErr = "Only letters, dashes, apostrophes and whitespace are allowed!";
    }
  }

  if (empty($_POST["gender"])) {
    $genderErr = "Gender is required.";
  } else {
    $gender = sanitize($_POST["gender"]); // same as $_REQUEST["gender"]
  }

  if (empty($_POST["email"])) {
    $emailErr = "Email is required.";
  } else {
    $email = sanitize($_POST["email"]); // same as $_REQUEST["email"]

    # 3 - filter_var()
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
      $emailErr = "Invalid email format";
    }
  }

  if (empty($_POST["website"])) {
    $website = "";
  } else {
    $website = sanitize($_POST["website"]); // same as $_REQUEST["website"]
    if (!preg_match(
      "/\b(?:(?:https?|ftp):\/\/|www\.)[-a-z0-9+&@#\/%?=~_|!:,.;]*[-a-z0-9+&@#\/%=~_|]/i", $website
    )) {
      $websiteErr = "Invalid URL format";
    }
  }

  if (empty($_POST["comment"])) {
    $comment = "";
  } else {
    $comment = sanitize($_POST["comment"]); // same as $_REQUEST["comment"]
  }
}
?>

// $_SERVER["PHP_SELF"]
// Saying the form (HTTP Request) will be sent to the current page itself
// Same site => Can display error message on the site where the form is.

// However, not hard-coding file name can lead to XSS vulnerability.
// On the server, PHP will populate $_SERVER["PHP_SELF"] with the filename
// of the current executing script. This "filename" is actually extracted from
// the URL. The URL can be rewritten with URL Encoding Characters to inject
// malicious code into the response script.

// Paste this URL into browser's address bar and see for yourself:
// http:/localhost:8000/index.php/%22%3E%3Cscript%3Ealert('hacked')%3C/script%3E

// %22%3E%3Cscript%3Ealert('hacked')%3C/script%3E
// corresponds to "><script>alert('hacked')</script>

<form method="post" action="<?php echo htmlspecialchars($_SERVER['PHP_SELF']); ?>">

  // Do I need to sanitize these variable again? Perhaps, if you accidentally forgot to sanitize it
  First Name:<input type="text" name="fname" value="<?php echo $fname; ?>" />
  <span class="error">* <?php echo $fnameErr ?? ""; ?></span><br />

  Last Name:<input type="text" name="lname" value="<?php echo $lname; ?>" />
  <span class="error">* <?php echo $lnameErr ?? ""; ?></span><br />

  Gender:
  <input type="radio" name="gender" value="female" <?php if (isset($gender) && $gender === "female") echo "checked"; ?> />Female
  <input type="radio" name="gender" value="male" <?php if (isset($gender) && $gender === "male") echo "checked"; ?> />Male
  <input type="radio" name="gender" value="other" <?php if (isset($gender) && $gender === "other") echo "checked"; ?> />Other
  <span class="error">* <?php echo $genderErr ?? ""; ?></span><br />

  Email: <input type="email" name="email" value="<?php echo $email; ?>" /><span class="error">* <?php echo $emailErr ?? ""; ?></span><br />

  Website: <input type="url" name="website" value="<?php echo $website; ?>" /><span class="error"><?php echo $websiteErr ?? ""; ?></span><br />

  Comment: <textarea name="comment" rows="5" cols="40"><?php echo $comment; ?></textarea><br />

  <input type="submit" value="Submit" />
</form>

/**
 * $_REQUEST
 *
 * An array contains variables from $_GET, $_POST and $_COOKIE
 *
 * $_GET
 * An array of variables received via HTTP GET method.
 * It gets populated from URL query parameter.
 *
 * $_POST
 * An array of variables received via HTTP POST method.
 * It gets populated from HTTP Request Body.
 *
 * Both GET or POST could produce the same result
 *
 * GET: used for data that are:
 * - Non-sensitive.
 * - Limited to 2000 characters.
 * - Bookmark-able.
 *
 * POST: used for data that are:
 * - Sensitive
 * - Unlimited.
 * - Not possible to bookmark.
 * - Needed for advanced functionality.
 */

// POST, HTML Forms
<form method="post" action="demo_post.php">
  First Name: <input type="text" name="fname" />
  <input type="submit"> // Since it's a non-AJAX method => Reload
</form>

// POST, JavaScript XMLHttpRequest()
<script>
  function sendRequest() {
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "demo_post.php");
    xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    // REMINDER: function declaration instead of arrow function
    // since `this` global variable must refer to xhttp obj
    xhttp.onload = function () {
      document.getElementById("demo").innerText = this.responseText;
    }
    // xhttp.send("fname=John");
    xhttp.send("fname=");   // what if name is empty?
  }
</script>

// GET, HTML Forms
<form method="GET" action="welcome.php">
  Name: <input type="text" name="name">
  Email: <input type="email" name="email">
  <input type="submit">
</form>

// welcome.php
// NOTE: No server-side validation and sanitization here
<?php echo "Welcome, " . $_GET["name"] . /* $_POST["name"] */ "<br/>" ?>
<?php echo "Your email address is " . $_GET["email"]; /* $_POST["email"] */ ?>

// GET, Query paramter
<a href="demo_get.php?subject=PHP&web=w3schools.com">Test GET request</a>

// demo_get.php
<?php
echo "Study " . $_REQUEST["subject"] . " at " . $_REQUEST["web"];
?>

/**
 * PHP include/require
 */
// based on functionality, they're the same. Differences:
// `require_once()` produce a fatal error and stop the script, therefore avoid compromising security and integrity. Used when the file is mandatory
// `include_once()` produce a warning and continue the script. Used the the file is not required.
<?php require_once("footer.php"); ?>
<?php require_once("menu.php"); ?>
<?php include_once("noFileExists.php"); ?> // still run

/**
 * PHP Cookies
 *
 * Lifecycle
 * 1. First load (setting)
 * - PHP sends the HTTP Response.
 * - Its header list contains "Set-Cookie" header
 * - Browser stores this cookie.
 * NOTE: $_COOKIE in HTML script in HTTP Response Body hasn't been populated with this cookie yet.
 *
 * 2. Second load (and every subsequent load)
 * - Browser auto embed the stored cookie in its HTTP Request Header when accessing the cookie's domain.
 * - At server, PHP populates $_COOKIE with the received cookie.
 * - If another `setcookie()` or `setrawcookie()` is called with the same name, the existing cookie is updated.
 */

// Create cookie
// Since Cookies are set via HTTP Headers, which must be sent before any responses. That's why setcookie() must be called before any HTML output
<?php
$cookieName = "user";
$cookieValue = "Jane Doe";
setcookie($cookieName, $cookieValue, time() + (86400 /* 1 day */ * 30), "/"); // Automatically URL encodes the value during transmission and decodes upon receipt
setrawcookie($cookieName, $cookieValue, time() + (86400 * 30), "/"); // // Prevent URL encoding when sending the cookie, but it can not contain a few characters
?>
// <!DOCTYPE html>
// <html>...

// How to use Cookies on First load (setting)
// => By setting $_COOKIE variable directly
<?php
// setcookie(...)
$_COOKIE[$cookieName] = $cookieValue;
?>
// Do not use cookie value directly from global variable.
// What if it's fetched from databases?

// Avoid unnecessary cookies setting
<?php
// only set the cookie if it doesn't exist or has a diff value
if (!isset($_COOKIE[$cookieName]) || $_COOKIE[$cookieName] !== $cookieValue) {
  setcookie($cookieName, $cookieValue, time() + (86400 * 30), "/");
}
?>

// Delete cookie
// Set the same name cookie with a expiration date in the past
<?php
setcookie($cookieName, "", time() - 3600);
?>

// Check if cookie is enabled
// count the $_COOKIE array
<?php
if (count($_COOKIE) > 0) {
  echo "Cookies are enabled.";
} else {
  echo "Cookies are disabled.";
}
?>

// practical example to learn cookies
// TODO: read https://www.tutorialspoint.com/php/php_mysql_login.htm and
// https://www.tutorialspoint.com/php/php_mysql_login.htm

/**
 * PHP Session
 *
 * Cre: cassiomolin https://stackoverflow.com/a/54785276/9122512
 *
 * HTTP is a stateless protocol, where each request from client to server
 * (should) contains all of the information necessary to for the server to
 * understand the request, without taking any advantage of any stored context
 * on the server. (from RFC 7230)
 *
 * Mechanism for state management in HTTP, such as cookies, allowing session
 * management on server side. But logically speaking it doesn't make HTTP
 * stateful. (from RFC 6265)
 *
 * PHP introduces $_SESSION[] superglobal.
 * It can store user information and its data can be accessed from multiple web pages. * It's best method to hold information about a single user.
 *
 */

// demo_session.php
<?php
// Just like cookies, it must be the very first thing in the document
session_start();
?>
<?php
$_SESSION["favColor"] = "lavender";
$_SESSION["favAnimal"] = "cat";
echo "Session variables are set!";

// modify
$_SESSION["favColor"] = "black";
?>

// demo_session2.php
<?php
// session variables are not passed individually to each new page
// they are retrieved from the session we open at the beginning
// of each page
session_start();
?>
<?php
echo "Here are the session variables:", "<br/>";
echo "favColor: " . $_SESSION["favColor"] . "<br/>";
echo "favAnimal: " . $_SESSION["favAnimal"] . "<br/>";
print_r($_SESSION);

// remove all session variables
session_unset();

// destroy the session
session_destroy();
?>

// Behind the scene:
// Browser create a "session" cookie
// (i.e. Cookie whose Expires/Max Age is "Session")
// whose value is similar to this: "765487cf34ert8dede5a562e4f3a7e12".
// It's called a user-key, when a session is opened on another page, browsers
// scan the computer for a user-key and if there's a match, it accesses that
// session, if not it creates a new session

/**
 * PHP Filters
 *
 * There are other built-in functions that can work as a validate function
 * such as is_int() and is_numeric(). However, filter functions are design to
 * validate specific for user input, which is always a string.
 *
 */
 <table>
  <tr>
    <th>Filter Name</th>
    <th>Filter ID</th>
  </tr>
  <?php
  foreach (filter_list() as $id => $filter) {
    echo "<tr><td>" . $filter . "</td><td>" . filter_id($filter) . "</td></tr>";
  }
  ?>
</table>

<?php
// Validate a string
$str = "<h1>Hello World!</h1>";
$newstr = filter_var($str, FILTER_SANITIZE_STRING);
echo $str;
// NOTE: DO NOT USE, it has been depreciated since PHP 8.1.
// Use htmlspecialchars() instead
?>

<?php
$int = "0";
// filter_var(0, FILTER_VALIDATE_INT) = 0
if (
  filter_var($int, FILTER_VALIDATE_INT) === 0
  || !filter_var($int, FILTER_VALIDATE_INT) === false
) {
  echo "Integer is valid";
} else {
  echo "Integer is not valid";
}
?>

<?php
// Validate an IP address
$ip = "127.0.0.1";

if (!filter_var($ip, FILTER_VALIDATE_IP) === false) {
  echo "$ip is a valid IP address";
} else {
  echo "$ip is not a valid IP address";
}
?>

<?php
// Sanitize and Validate an email address
$email = "john.doe@example.@";

// Sanitize email
$email = filter_var($email, FILTER_SANITIZE_EMAIL);

// Validate email
if (!filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
  echo "$email is a valid email address.";
} else {
  echo "$email is not a valid email address.";
}
?>

<?php
// Sanitize and Validate a URL
$url = "https://example.com";

// sanitize
$url = filter_var($url, FILTER_SANITIZE_URL);

// validate
if (!filter_var($url, FILTER_VALIDATE_URL) === false) {
  echo "$url is a valid URL";
} else {
  echo "$url is not a valid URL";
}
?>

/**
 * PHP Advanced Filtering
 */
<?php
// validate an integer within a range
$int = 1;
$min = 1;
$max = 200;

if (!filter_var($int, FILTER_VALIDATE_INT, [
  "options" => [
    "min_range" => $min,
    "max_range" => $max
  ]
]) === false) {
  echo "$int is within range";
} else {
  echo "$int is not within range";
}
?>


<?php
// Validate a URL must contain query string
$url = "example.com/?abc=1&def=2";

if (!filter_var($url, FILTER_VALIDATE_URL, FILTER_FLAG_QUERY_REQUIRED) === false) {
  echo "$url is a valid URL with a query string!";
} else {
  echo "$url is not a valid URL or a valid one without query string!";
}
?>

/**
 * Callback Function
 *
 * PHP is a multi-paradigm now, huh?
 */

<?php
function my_callback($item) {
  return strlen($item);
}

$strings = ["apple", "orange", "banana", "coconut"];
$lengths = array_map("my_callback", $strings);
print_r($lengths);

// anonymous function
$lengths = array_map(function ($item) {
  return strlen($item);
}, $strings);
print_r($lengths);
?>

<?php
function exclaim($str) {
  return $str . "! ";
}

function ask($str) {
  return $str . "? ";
}

function printFormatted($str, $format) {
  // Calling the $format callback function
  echo $format($str);
}

// Pass "exclaim" and "ask" as callback functions to printFormatted()
printFormatted("Hello world", "exclaim");
printFormatted("Hello world", "ask");
?>

/**
 * PHP JSON
 */
<?php
$age = [
  "Harry" => 35,
  "Ben" => 37,
  "John" => 49
];
$brands = [
  "Volvo",
  "Toyota",
  "BMW"
];

echo json_encode($age), BR;
echo json_encode($brands), BR;

$json = '{"Harry":35,"Ben":37,"John":49}';
$obj = json_decode($json);
var_dump($obj); // PHP object, stdClass
echo $obj->Harry, BR;
echo $obj->Ben, BR;
echo $obj->John, BR;

echo BR;

$arr = json_decode($json, true);
var_dump($arr); // Associative array
echo $arr["Harry"], BR;
echo $arr["Ben"], BR;
echo $arr["John"], BR;
?>

/**
 * PHP Exception
 */
<?php
function divide($dividend, $divisor) {
  if ($divisor === 0) {
    throw new \Exception("Division by zero");
  }
  return $dividend / $divisor;
}

try {
  echo divide(1, 0), BR;
} catch (\Exception $ex) {
  echo "Unable to divide.", BR;
  $code = $ex->getCode();
  $message = $ex->getMessage();
  $file = $ex->getFile();
  $line = $ex->getLine();
  echo "Exception thrown in $file on line $line: [Code $code]
  $message";
} finally {
  echo "Process complete.", BR;
}
?>
```

## OOP

```php
<?php
const BR = "<br />";

/**
 * PHP Class
 */

// final will prevent class inheritance
/* final */
class Fruit {
  public const LEAVING_MESSAGE = "Thank you for learning PHP.";

  // fields/properties
  // access modifier: protected
  protected string $name;
  protected string $color;
  protected int $weight;

  // constructor
  // no access modifier -> public
  function __construct($name = "", $color = "", $weight = 0) {
    // DO NOT VALIDATE DATA HERE
    $this->name = $name;
    $this->color = $color;
    $this->weight = $weight;
  }

  // destructor
  // automatically called when the object is no longer referenced
  // or when the script terminates
  function __destruct() {
    // Curly braces
    // They're necessary in the following situations:
    // - When the variable is immediately followed by characters that could be
    // part of a variable name.
    // E.g. echo "The fruits are {$this->name}s."
    //
    // - When using more complex expressions or property/method access.
    // E.g. echo "The fruit is {this->getName()}."
    //
    // When disambiguating object properties and array accesses
    // E.g. echo "The fruit is {this->arr["name"]}."
    echo "{$this->name} is eaten.", BR;
    echo self::LEAVING_MESSAGE, BR;
  }

  // methods

  // prevent method overriding
  protected /* final */ function printIntro(): void {
    echo "The fruit is {$this->name} and the color is {$this->color}.", BR;
  }

  function setColor($color): void {
    // data validation logic here...
    // $this keyword refers to the current object
    // only accessible from within methods
    $this->color = $color;
  }

  function getColor(): string {
    return $this->color;
  }

  function setName($name): void {
    // data validation logic here...
    $this->name = $name;
  }

  function getName(): string {
    return $this->name;
  }
}

// Strawberry is inherited from Fruit
class Strawberry extends Fruit {

  public function printIntro(): void {
    echo "The fruit is {$this->name} and the color is {$this->color} and the
    weight is {$this->weight}.", BR;
  }

  public function printMessage() {
    $this->printIntro(); // calls protected method from within the derived class
    echo "Am I a straw, a berry, or both?", BR;
  }
}

$apple = new Fruit();
$apple->setName("apple");
$apple->setColor("red");
echo "Name: " . $apple->getName() . BR;
echo "Color: " . $apple->getColor() . BR;
var_dump($apple instanceof Fruit);

$banana = new Fruit("banana", "yellow");
echo "Name: " . $banana->getName() . BR;
echo "Color: " . $banana->getColor() . BR;

$strawberry = new Strawberry("strawberry", "red", 300);
$strawberry->printMessage();
echo Fruit::LEAVING_MESSAGE, BR;


/**
 * PHP Abstract Class
 *
 * Class that can't be instantiated directly.
 * Define at least one abstract method.
 * Abstract method must either be protected or public (duh!)
 * Refers to as "Abstraction" - 1 of 4 pillars of OOP.
 *
 * When a child class is inherited from an abstract class:
 * - Child class method must be defined with the same name, and it redeclares
 * the parent abstract method.
 * - Child class method must be defined with the same or less restrictive access
 * modifier
 * - The number of required arguments must be the same. However, the child class
 * can introduce optional arguments in addition.
 */

abstract class ParentClass {
  abstract public function abstructMethod1($reqParam);
  public function method2() {
    // ...
  }
}

class ChildClass extends ParentClass {
  public function abstractMethod1($reqParam, $optParam="") {
    // ...
  }
}

/**
 * PHP Interfaces
 *
 * What methods a class (or multiple classes) should implement?
 * Make it easy to use a variety of different classes in the same way.
 * Refers to as "polymorphism" - 1 of 4 pillars of OOP.
 *
 * Interfaces vs. Abstract Classes
 * - Interfaces can't have fields, Abstract Classes can.
 * - Interfaces' methods must be public, so the public keyword is unnecessary,
 * Abstract Classes' methods are public or protected.
 * - All methods in an interface are abstract, the abstract keyword is redundant
 * - Classes can implement both an interface and a class at the same time.
 */
interface Animal {
  public function makeSound();
}

class Cat implements Animal {
  public function makeSound() {
    echo "Meowwww!";
  }
}

class Dog implements Animal {
  public function makeSound() {
    echo "Woofff!";
  }
}

// PHP is loosely-typed, so it's required concrete type declaration like Java so
// it might be hard to realize that when working with a group of animals, even
// if we don't know which species are they, we only care that they can make
// sounds.

/**
 * PHP Trait
 *
 * PHP only supports single inheritance, like Java did.
 * However, PHP allows class to inherit multiple behavior with the concept of
 * trait.
 */
trait msg1 {
  public function msg1() {
    // ...
  }
}

trait msg2 {
  public function msg2() {
    // ...
  }
}

class Welcome1 {
  use msg1;
}

class Welcome2 {
  use msg1, msg2;
}

// Welcome1 now possess msg1() method.
// Welcome2 now possess both msg1() and msg2() methods.

// To know when and where to use Abstract Class or Interface is an art.
// There is a field called Object Oriented Analysis Design (OOAD) that revolves
// around this problem.

/**
 * PHP Static Method and Static Properties
 */
class Greeting {
  public static $staticProperty = "PHP";

  public static function welcome() {
    echo "Hello!, {self::$staticProperty}";
  }

  public function __construct() {
    // self and scope resolution operator
    self::welcome();
  }
}

class SuperGreeting extends Greeting {
  public function callStatic() {
    echo parent::$staticProperty;
  }
}

// class name and scope resolution operator
Greeting::welcome();
echo Greeting::$staticProperty;

/**
 * PHP Namespace
 *
 * Qualifiers that solve 2 problems:
 * - Better organization by grouping classes that work together to perform a task
 * - Prevent name collision by allowing the same name to be used for more than
 * one class.
 *
 * NOTE: namespace declaration statement must be THE VERY FIRST statement, OR
 * after any declare() call.
 */

// Any code that follows a `namespace` declaration lies inside that namespace:
// - You can create object by referring class name directly without prefixing it
// with namespace.
// - But, when referring to entities that existed only in Global Namespace (e.g.
// Exception), you must prefixed it with a backslash.
namespace Math;

function divide($dividend, $divisor) {
  if ($divisor === 0) {
    // Notice the backslash
    // Without it, PHP will resolve to an Exception class from Math namespace.
    throw new \Exception("Division by zero");
  }
  return $dividend / $divisor;
}

// In the case of callback, regardless of the code being subsequent to namespace
// declaration, you must prefix all callback function with backslash.
namespace MyApp;
// namespace MyApp\Furniture // Nested namespace

function getNamespace() {
  return __NAMESPACE__; // predefined constant
}

function processData($data) {
  return "Processed: $data";
}

$arr = ["item1", "item2", "item3"];
$res1 = array_map("processData", $arr); // FAIL
// NOTE: double backslash if wrapped inside double quotes
$res2 = array_map("MyApp\\processData", $arr); // WORKS
$res3 = array_map(__NAMESPACE__ . "\\processData", $arr); // ALSO WORKS

// If a PHP file with namespace is included/required
// The importer will have to specify the namespace
require_once("demo_namespace.php");
$table = new Html\Table();
$row = new Html\Row();

/**
 * PHP Iterables
 *
 * Basically, any value that can be looped through with a foreach loop.
 *
 * Built-in iterables are: indexed array and associative array
 * Custom iterable is a class that implements Iterator interface and realizes
 * all of its method.
 */

function printIterable(iterable $myIterable) {
  // indexed array
  foreach ($myIterable as $item) {
    echo $item, BR;
  }
}

function printIterable2(iterable $myIterable) {
  // associative array
  foreach ($myIterable as $key => $item) {
    echo $key, ": ", $item, BR;
  }
}

$arr = [1, 2, 3, 4, 5];
printIterable($arr);

$arr2 = ["a" => 1, "b" => 2, "c" => 3];
printIterable2($arr2);

function getIterable(): iterable {
  return ["a", "b", "c"];
}

$myIterable = getIterable();
foreach ($myIterable as $item) {
  echo $item, BR;
}

// Create an Iterator
class MyIterator implements Iterator {
  private $items = [];
  private $pointer = 0;

  public function __construct($items) {
    // array_values() makes sure that the keys are numbers
    $this->items = array_values($items);
  }

  // return the element that the pointer is currently pointing to
  // it's like the index of an indexed array
  public function current(): mixed {
    return $this->items[$this->pointer];
  }

  // returns the key associated with the current element in the list
  // it can be integer, float, bool or string
  public function key(): mixed {
    return $this->pointer;
  }

  // Moves the pointer to the next element in the list
  public function next(): void {
    $this->pointer++;
  }

  // Moves the pointer to the first element in the list
  public function rewind(): void {
    $this->pointer = 0;
  }

  // If the internal pointer is not pointing to any element, it should return
  // false. Otherwise, return true.
  public function valid(): bool {
    // count() indicates how many items are in the list
    return $this->pointer < count($this->items);
  }
}

// Use the iterator as an iterable
$iterator = new MyIterator(["a", "b", "c"]);
printIterable($iterator);
?>
```

## Database

```php
/**
 * MySQL
 *
 * MySQL is the M in LAMP stack (Linux, Apache, MySQL/MariaDB, PHP).
 *
 * Pros:
 * - The most popular database system.
 * - Used for web application (if not, static HTML is enough).
 * - Runs on a server, hence the name Database Server (but again, it's just a
 * computer that install MySQL)
 * - Fast, reliable, ideal for both small and large apps (ACID compliant, ...)
 * I prefer SQLite for since it has a steeper learning curve.
 * - Used Standard SQL (as oppose to T-SQL, PostgreSQL, PL/SQL, ...)
 * - FOSS.
 * - Developed, distributed and supported by Oracle
 * - MySQL is named after co-founder Monty Widenius's daughter: My.
 * - His later creation, MariaDB, is also taken after his 2nd daughter: Maria.
 */

/**
 * PHP connection to MySQL
 *
 * There are 2 libraries: MySQLi ("i" stands for improved) and PDO (PHP Data
 * Object)
 *
 * MySQLi vs. PDO
 * - MySQLi only works with MySQL database. PDO works with 12 different database
 * systems.
 * - Both are OO, MySQLi provides a procedural API.
 * - Both support Prepared Statements that protect from SQL injection.
 */

```
