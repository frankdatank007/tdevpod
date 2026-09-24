-- Rainbow.hs: a pure, lazy rainbow (pretend, never compiled)
module Rainbow where

import Data.List (intercalate)

data Color = Red | Orange | Yellow | Green | Blue | Indigo | Violet
  deriving (Show, Eq, Enum, Bounded)

rainbow :: [Color]
rainbow = [minBound .. maxBound]

stripe :: Int -> Color -> String
stripe width c = replicate width '~' ++ " " ++ show c

paint :: Int -> String
paint width = intercalate "\n" (map (stripe width) rainbow)

countStripes :: [Color] -> Int
countStripes = foldr (\_ acc -> acc + 1) 0

main :: IO ()
main = do
  putStrLn (paint 12)
  putStrLn ("stripes: " ++ show (countStripes rainbow))
  mapM_ print (filter (/= Indigo) rainbow)
