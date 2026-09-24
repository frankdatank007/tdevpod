# snack_bar.rb: a tiny snack counter (display-only theatre)
require "json"

class Snack
  attr_reader :name, :crunch

  def initialize(name, crunch: 5)
    @name = name
    @crunch = crunch
  end

  def to_s
    "#{name} (crunch #{crunch}/10)"
  end
end

MENU = [
  Snack.new("apple slices", crunch: 7),
  Snack.new("cheese stick", crunch: 1),
  Snack.new("goldfish crackers", crunch: 9),
  Snack.new("banana", crunch: 0)
].freeze

def order(*names)
  MENU.select { |s| names.include?(s.name) }
      .sort_by(&:crunch)
      .reverse
end

order("banana", "goldfish crackers").each do |snack|
  puts "one #{snack}, coming right up"
end

puts JSON.pretty_generate(menu: MENU.map(&:name))
