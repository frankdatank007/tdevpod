# train_yard.ex: a toy train dispatcher (pretend, never compiled)
defmodule TrainYard do
  @moduledoc "Chugga chugga, choo choo."

  defstruct engine: "blue", cars: [], whistle: true

  def couple(%TrainYard{cars: cars} = train, car) do
    %{train | cars: cars ++ [car]}
  end

  def depart(%TrainYard{whistle: true} = train) do
    IO.puts("TOOT TOOT! #{train.engine} engine leaving with #{length(train.cars)} cars")
    {:ok, train}
  end

  def depart(_train), do: {:error, :no_whistle}

  def run do
    ~w(teddy blocks crayons juice)
    |> Enum.reduce(%TrainYard{}, &couple(&2, &1))
    |> depart()
    |> case do
      {:ok, _} -> IO.puts("next stop: the couch")
      {:error, why} -> IO.inspect(why)
    end
  end
end
