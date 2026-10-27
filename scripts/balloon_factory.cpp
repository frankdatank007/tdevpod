// balloon_factory.cpp: puff up balloons, then tie a bow (never runs)
#include <iostream>
#include <string>
#include <vector>

struct Balloon {
    std::string color;
    int air = 0;
    bool floating() const { return air >= 100; }
};

std::string bar(int pct) {
    int filled = pct / 5;
    return "[" + std::string(filled, '#') + std::string(20 - filled, '-') + "]";
}

int main() {
    std::vector<Balloon> bunch = {{"red"}, {"green"}, {"purple"}};
    for (auto& b : bunch) {
        while (!b.floating()) {
            b.air += 5;
            std::cout << '\r' << bar(b.air) << ' ' << b.air << "%  puffing " << b.color;
        }
    }
    std::cout << "\nbunch floats away. bye bye!\n";
    return 0;
}

// $ g++ balloon_factory.cpp && ./a.out

// ── output ────────────────────────────────────────────
[--------------------]   0%  puffing red balloon
[#-------------------]   5%  puffing red balloon
[##------------------]  10%  puffing red balloon
[###-----------------]  15%  puffing red balloon
[####----------------]  20%  puffing red balloon
[#####---------------]  25%  puffing red balloon
[######--------------]  30%  puffing red balloon
[#######-------------]  35%  puffing red balloon
[########------------]  40%  puffing red balloon
[#########-----------]  45%  puffing red balloon
[##########----------]  50%  puffing red balloon
[###########---------]  55%  puffing red balloon
[############--------]  60%  puffing red balloon
[#############-------]  65%  puffing red balloon
[##############------]  70%  puffing red balloon
[###############-----]  75%  puffing red balloon
[################----]  80%  puffing red balloon
[#################---]  85%  puffing red balloon
[##################--]  90%  puffing red balloon
[###################-]  95%  puffing red balloon
[####################] 100%  puffing red balloon
✔ red balloon floats
◒ tying a bow on red...
◐ tying a bow on red...
◓ tying a bow on red...
◑ tying a bow on red...
◒ tying a bow on red...
◐ tying a bow on red...
◓ tying a bow on red...
◑ tying a bow on red...
◒ tying a bow on red...
◐ tying a bow on red...
◓ tying a bow on red...
◑ tying a bow on red...
→ next up!
[--------------------]   0%  puffing green balloon
[##------------------]  10%  puffing green balloon
[####----------------]  20%  puffing green balloon
[######--------------]  30%  puffing green balloon
[########------------]  40%  puffing green balloon
[##########----------]  50%  puffing green balloon
[############--------]  60%  puffing green balloon
[##############------]  70%  puffing green balloon
[################----]  80%  puffing green balloon
[##################--]  90%  puffing green balloon
[####################] 100%  puffing green balloon
✔ green balloon floats
⠋ finding the purple balloon...
⠙ finding the purple balloon...
⠹ finding the purple balloon...
⠸ finding the purple balloon...
⠼ finding the purple balloon...
⠴ finding the purple balloon...
⠦ finding the purple balloon...
⠧ finding the purple balloon...
⠇ finding the purple balloon...
⠏ finding the purple balloon...
⠋ finding the purple balloon...
⠙ finding the purple balloon...
⠹ finding the purple balloon...
⠸ finding the purple balloon...
⠼ finding the purple balloon...
⠴ finding the purple balloon...
⠦ finding the purple balloon...
⠧ finding the purple balloon...
⠇ finding the purple balloon...
⠏ finding the purple balloon...
→ next up!
[--------------------]   0%  puffing purple balloon
[#-------------------]   5%  puffing purple balloon
[##------------------]  10%  puffing purple balloon
[###-----------------]  15%  puffing purple balloon
[####----------------]  20%  puffing purple balloon
[#####---------------]  25%  puffing purple balloon
[######--------------]  30%  puffing purple balloon
[#######-------------]  35%  puffing purple balloon
[########------------]  40%  puffing purple balloon
[#########-----------]  45%  puffing purple balloon
[##########----------]  50%  puffing purple balloon
[###########---------]  55%  puffing purple balloon
[############--------]  60%  puffing purple balloon
[#############-------]  65%  puffing purple balloon
[##############------]  70%  puffing purple balloon
[###############-----]  75%  puffing purple balloon
[################----]  80%  puffing purple balloon
[#################---]  85%  puffing purple balloon
[##################--]  90%  puffing purple balloon
[###################-]  95%  puffing purple balloon
[####################] 100%  puffing purple balloon
✔ 3 balloons floating, 0 pops
