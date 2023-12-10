import Data.Char (isDigit)
import Data.Maybe (mapMaybe)

getFirstAndLastDigit :: String -> Maybe (Char, Char)
getFirstAndLastDigit input =
  case filter isDigit input of
    []     -> Nothing
    digits -> Just (head digits, last digits)

-- Convert Maybe (Char, Char) to Maybe Int
digitsToNumber :: Maybe (Char, Char) -> Maybe Int
digitsToNumber maybeDigits = do
  (firstDigit, lastDigit) <- maybeDigits
  let numberStr = [firstDigit, lastDigit]
  pure (read numberStr :: Int)

main :: IO ()
main = do
  -- Read input from the file
  contents <- readFile "input.txt"

  -- Split the contents into lines and apply the function to each line
  let inputs = lines contents
  let digits = map getFirstAndLastDigit inputs

  -- Extract digits and create a list of numbers
  let calibrationValues = mapMaybe digitsToNumber digits

  -- Calculate and print the sum of numbers
  print (sum calibrationValues)

