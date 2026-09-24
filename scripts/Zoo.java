// Zoo.java: a pretend zoo keeper (never compiled, only drawn)
package pod.zoo;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Zoo {
    private final List<Animal> animals = new ArrayList<>();

    record Animal(String name, String sound, int naps) {}

    public void admit(String name, String sound) {
        animals.add(new Animal(name, sound, 0));
        System.out.println("welcome, " + name + "!");
    }

    public Map<String, String> chorus() {
        Map<String, String> sounds = new java.util.TreeMap<>();
        for (Animal a : animals) {
            sounds.put(a.name(), a.sound().toUpperCase());
        }
        return sounds;
    }

    public static void main(String[] args) {
        Zoo zoo = new Zoo();
        zoo.admit("lion", "roar");
        zoo.admit("duck", "quack");
        zoo.admit("cow", "moo");
        zoo.admit("owl", "hoo");
        zoo.chorus().forEach((who, says) ->
            System.out.printf("%s says %s%n", who, says));
    }
}
