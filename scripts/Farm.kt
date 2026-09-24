// Farm.kt: morning chores on a pretend farm (display-only)
package pod.farm

enum class Chore(val minutes: Int) {
    FEED_CHICKENS(5),
    MILK_COW(10),
    COLLECT_EGGS(3),
    BRUSH_PONY(8)
}

data class Farmer(val name: String, var boots: Boolean = false)

fun Farmer.doChores(chores: List<Chore>): Int {
    if (!boots) {
        println("$name puts on muddy boots")
        boots = true
    }
    return chores.sumOf { it.minutes }
}

fun main() {
    val farmer = Farmer("Little Farmer")
    val today = Chore.entries.shuffled().take(3)
    val total = farmer.doChores(today)

    today.forEachIndexed { i, chore ->
        println("${i + 1}. ${chore.name.lowercase().replace('_', ' ')}")
    }
    println("all done in $total minutes, time for pancakes")
}
