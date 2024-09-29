#include <stxs>;

clear; >/ clear the screen before first frame load;
int delay = 1;
string greeting = "Loading Resources...";
disp (greeting);
wait (delay);

>/ comment support finally!;

int i = 3;
int j = 0;
repeat (i){
 j += 1,
 clear,
 disp ("J: "),
 disp (j),
 disp ("Sorting sheep..."),
 disp ("Making honey..."),
 disp ("Writing code..."),
 wait (delay)
};

clear;
if (j >= i){
 disp ("J is greater than I.")
};

<!>

nothing below the termination string is compiled!!

1xs
2r
3p