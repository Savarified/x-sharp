#include <stxs>;
#include <window>;

string title = "Window test";
disp (title);

window (600,400);
window.name = "My first window!";
window.fill "red";

window.run;
<!>