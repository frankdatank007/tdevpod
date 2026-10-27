// space_elevator.rs: a cable car up to the moon, with snacks (never runs)
use std::{thread, time::Duration};

const SPINNER: [char; 10] = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];

struct Car {
    floor: u32,
    snacks: Vec<&'static str>,
}

impl Car {
    fn climb(&mut self, floors: u32) {
        self.floor = (self.floor + floors).min(100);
    }
}

fn bar(pct: u32) -> String {
    let filled = (pct / 5) as usize;
    let mut s = "█".repeat(filled);
    if filled < 20 {
        s.push('▓');
    }
    format!("[{:░<20}]", s)
}

fn main() {
    let mut car = Car { floor: 0, snacks: vec!["cookie", "banana", "star"] };
    while car.floor < 100 {
        car.climb(4);
        println!("{} {:3}% climbing", bar(car.floor), car.floor);
        thread::sleep(Duration::from_millis(90));
    }
    println!("welcome to the moon, {} snacks left", car.snacks.len());
}

// $ cargo run

// ── output ────────────────────────────────────────────
⠋ checking the cable is still attached...
⠙ checking the cable is still attached...
⠹ checking the cable is still attached...
⠸ checking the cable is still attached...
⠼ checking the cable is still attached...
⠴ checking the cable is still attached...
⠦ checking the cable is still attached...
⠧ checking the cable is still attached...
⠇ checking the cable is still attached...
⠏ checking the cable is still attached...
⠋ checking the cable is still attached...
⠙ checking the cable is still attached...
⠹ checking the cable is still attached...
⠸ checking the cable is still attached...
⠼ checking the cable is still attached...
⠴ checking the cable is still attached...
⠦ checking the cable is still attached...
⠧ checking the cable is still attached...
⠇ checking the cable is still attached...
⠏ checking the cable is still attached...
✔ cable attached to the moon
[▓▒░░░░░░░░░░░░░░░░░░]   0%  climbing past the clouds
[▓▒░░░░░░░░░░░░░░░░░░]   4%  climbing past the clouds
[█▓▒░░░░░░░░░░░░░░░░░]   8%  climbing past the clouds
[██▓▒░░░░░░░░░░░░░░░░]  12%  climbing past the clouds
[███▓▒░░░░░░░░░░░░░░░]  16%  climbing past the clouds
[████▓▒░░░░░░░░░░░░░░]  20%  climbing past the clouds
[████▓▒░░░░░░░░░░░░░░]  24%  climbing past the clouds
[█████▓▒░░░░░░░░░░░░░]  28%  climbing past the clouds
[██████▓▒░░░░░░░░░░░░]  32%  climbing past the clouds
[███████▓▒░░░░░░░░░░░]  36%  climbing past the clouds
[████████▓▒░░░░░░░░░░]  40%  climbing past the clouds
[████████▓▒░░░░░░░░░░]  44%  climbing past the clouds
[█████████▓▒░░░░░░░░░]  48%  climbing past the clouds
[██████████▓▒░░░░░░░░]  52%  climbing past the clouds
[███████████▓▒░░░░░░░]  56%  climbing past the clouds
[████████████▓▒░░░░░░]  60%  climbing past the clouds
[████████████▓▒░░░░░░]  64%  climbing past the clouds
[█████████████▓▒░░░░░]  68%  climbing past the clouds
[██████████████▓▒░░░░]  72%  climbing past the clouds
[███████████████▓▒░░░]  76%  climbing past the clouds
[████████████████▓▒░░]  80%  climbing past the clouds
[████████████████▓▒░░]  84%  climbing past the clouds
[█████████████████▓▒░]  88%  climbing past the clouds
[██████████████████▓▒]  92%  climbing past the clouds
[███████████████████▓]  96%  climbing past the clouds
[████████████████████] 100%  climbing past the clouds
✔ clouds: 12, birds waved at: 7
⠏ counting stars on the way up...
⠇ counting stars on the way up...
⠧ counting stars on the way up...
⠦ counting stars on the way up...
⠴ counting stars on the way up...
⠼ counting stars on the way up...
⠸ counting stars on the way up...
⠹ counting stars on the way up...
⠙ counting stars on the way up...
⠋ counting stars on the way up...
⠏ counting stars on the way up...
⠇ counting stars on the way up...
⠧ counting stars on the way up...
⠦ counting stars on the way up...
⠴ counting stars on the way up...
⠼ counting stars on the way up...
⠸ counting stars on the way up...
⠹ counting stars on the way up...
⠙ counting stars on the way up...
⠋ counting stars on the way up...
→ next up!
[▓▒░░░░░░░░░░░░░░░░░░]   0%  climbing past the stars
[▓▒░░░░░░░░░░░░░░░░░░]   4%  climbing past the stars
[█▓▒░░░░░░░░░░░░░░░░░]   8%  climbing past the stars
[██▓▒░░░░░░░░░░░░░░░░]  12%  climbing past the stars
[███▓▒░░░░░░░░░░░░░░░]  16%  climbing past the stars
[████▓▒░░░░░░░░░░░░░░]  20%  climbing past the stars
[████▓▒░░░░░░░░░░░░░░]  24%  climbing past the stars
[█████▓▒░░░░░░░░░░░░░]  28%  climbing past the stars
[██████▓▒░░░░░░░░░░░░]  32%  climbing past the stars
[███████▓▒░░░░░░░░░░░]  36%  climbing past the stars
[████████▓▒░░░░░░░░░░]  40%  climbing past the stars
[████████▓▒░░░░░░░░░░]  44%  climbing past the stars
[█████████▓▒░░░░░░░░░]  48%  climbing past the stars
[██████████▓▒░░░░░░░░]  52%  climbing past the stars
[███████████▓▒░░░░░░░]  56%  climbing past the stars
[████████████▓▒░░░░░░]  60%  climbing past the stars
[████████████▓▒░░░░░░]  64%  climbing past the stars
[█████████████▓▒░░░░░]  68%  climbing past the stars
[██████████████▓▒░░░░]  72%  climbing past the stars
[███████████████▓▒░░░]  76%  climbing past the stars
[████████████████▓▒░░]  80%  climbing past the stars
[████████████████▓▒░░]  84%  climbing past the stars
[█████████████████▓▒░]  88%  climbing past the stars
[██████████████████▓▒]  92%  climbing past the stars
[███████████████████▓]  96%  climbing past the stars
[████████████████████] 100%  climbing past the stars
✔ arrived at the moon, 3 snacks left
