set textToType to "Hello, World!" -- Replace with your selection of 100 words
set delayBetweenCharacters to 0.1 -- Adjust the delay as needed

set keystrokesList to {}
set timestampsList to {}

tell application "System Events"
	repeat with i from 1 to length of textToType
		set currentCharacter to character i of textToType
		set startTime to (current date)
		keystroke currentCharacter
		delay delayBetweenCharacters
		set endTime to (current date)
		
		set endTimestamp to (time of endTime) * 1000 -- Convert to milliseconds
		set startTimestamp to (time of startTime) * 1000 -- Convert to milliseconds
		set timeDifference to endTimestamp - startTimestamp
		
		set endTimestampString to (endTimestamp as string)
		set startTimestampString to (startTimestamp as string)
		set timeDifferenceString to (timeDifference as string)
		
		set end of keystrokesList to currentCharacter
		set end of timestampsList to {startTimestampString, endTimestampString, timeDifferenceString}
	end repeat
end tell

-- Display the recorded keystrokes and timestamps
repeat with i from 1 to count of keystrokesList
	set currentKeystroke to item i of keystrokesList
	set currentTimestamps to item i of timestampsList
	set startTime to item 1 of currentTimestamps
	set endTime to item 2 of currentTimestamps
	set timeDifference to item 3 of currentTimestamps
	
	display dialog "Keystroke: " & currentKeystroke & return & "Start Time: " & startTime & return & "End Time: " & endTime & return & "Time Difference: " & timeDifference
end repeat

### VERSION 2
set textToType to "Hello, World!" -- Replace with your selection of 100 words
set delayBetweenCharacters to 0.1 -- Adjust the delay as needed

set recordedData to {}

tell application "System Events"
	repeat with i from 1 to length of textToType
		set currentCharacter to character i of textToType
		set startTime to (do shell script "date +%s.%N | awk '{printf \"%f\", $0}'")
		keystroke currentCharacter
		delay delayBetweenCharacters
		set endTime to (do shell script "date +%s.%N | awk '{printf \"%f\", $0}'")
		
		set startTimestamp to startTime as real
		set endTimestamp to endTime as real
		set timeDifference to endTimestamp - startTimestamp
		
		set end of recordedData to {typedCharacter:currentCharacter, startTime:startTimestamp, endTime:endTimestamp, timeDifference:timeDifference}
	end repeat
end tell

return recordedData


### VERSION 3
