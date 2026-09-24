/* robot_arm.c: firmware for a block-stacking robot (pretend, never built) */
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define MAX_BLOCKS 8
#define GRIP_STRENGTH 42

typedef struct {
    uint8_t height;
    const char *color;
} Block;

static Block tower[MAX_BLOCKS];
static int top = 0;

bool stack(const char *color) {
    if (top >= MAX_BLOCKS) {
        printf("tower too tall! wobble wobble\n");
        return false;
    }
    tower[top].height = top + 1;
    tower[top].color = color;
    top++;
    return true;
}

void knock_down(void) {
    while (top > 0) {
        printf("crash: %s block\n", tower[--top].color);
    }
}

int main(void) {
    const char *colors[] = {"red", "blue", "yellow", "green"};
    for (int i = 0; i < 10; i++) {
        stack(colors[i % 4]);
    }
    knock_down();
    return 0;
}
