import sys

# --- Data Structure Classes ---

class Patient:
    def __init__(self, patientId, name, age, severity):
        self.patientId = patientId
        self.name = name
        self.age = age
        self.severity = severity

class Token:
    def __init__(self, tokenId, patientId, doctorId, slotId, type):
        self.tokenId = tokenId
        self.patientId = patientId
        self.doctorId = doctorId
        self.slotId = slotId
        self.type = type

class Doctor:
    def __init__(self, doctorId, name, specialization):
        self.doctorId = doctorId
        self.name = name
        self.specialization = specialization

class SlotNode:
    def __init__(self, slotId, startTime, endTime, status):
        self.slotId = slotId
        self.startTime = startTime
        self.endTime = endTime
        self.status = status
        self.next = None

# --- Linked List for Doctor Schedule ---
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, slotId, startTime, endTime, status):
        # Time: O(1) - Insert at head
        # Space: O(1)
        newNode = SlotNode(slotId, startTime, endTime, status)
        newNode.next = self.head
        self.head = newNode

    def delete(self, slotId):
        # Time: O(k) - Traversal
        # Space: O(1)
        current = self.head
        previous = None
        
        while current is not None:
            if current.slotId == slotId:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
            
        return False

    def traverse(self):
        # Time: O(k)
        # Space: O(1)
        slots = []
        current = self.head
        while current is not None:
            # Storing data in a simple tuple
            data = (current.slotId, current.startTime, current.endTime, current.status)
            slots.append(data)
            current = current.next
        return slots

    def findNextFreeSlot(self):
        # Time: O(k)
        # Space: O(1)
        current = self.head
        while current is not None:
            if current.status == 'FREE':
                return current
            current = current.next
        return None

    def updateSlotStatus(self, slotId, status):
        # Time: O(k)
        # Space: O(1)
        current = self.head
        while current is not None:
            if current.slotId == slotId:
                current.status = status
                return True
            current = current.next
        return False

# --- Circular Queue for Routine Appointments ---
class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = [None] * capacity
        self.head = -1
        self.tail = -1

    def enqueue(self, token):
        # Time: O(1)
        # Space: O(1)
        
        # Calculating next position manually
        next_pos = (self.tail + 1) % self.capacity
        
        if next_pos == self.head:
            print("Queue Overflow")
            return False

        if self.head == -1:
            self.head = 0

        self.tail = next_pos
        self.queue[self.tail] = token
        return True

    def dequeue(self):
        # Time: O(1)
        # Space: O(1)
        if self.head == -1:
            return None

        token = self.queue[self.head]

        if self.head == self.tail:
            # Queue becomes empty here
            self.head = -1
            self.tail = -1
        else:
            self.head = (self.head + 1) % self.capacity

        return token

    def peek(self):
        if self.head == -1:
            return None
        return self.queue[self.head]

    def size(self):
        if self.head == -1:
            return 0
        if self.head <= self.tail:
            return self.tail - self.head + 1
        return self.capacity - self.head + self.tail + 1

# --- Min Heap for Emergency Triage ---
class MinHeap:
    def __init__(self):
        self.heap = []

    def _heapifyUp(self, index):
        # Time: O(log n)
        # Space: O(1)
        parentIndex = (index - 1) // 2
        
        # Comparing current node with parent (index 0 is severity)
        if index > 0:
            current_severity = self.heap[index][0]
            parent_severity = self.heap[parentIndex][0]
            
            if current_severity < parent_severity:
                # Swap manually
                temp = self.heap[index]
                self.heap[index] = self.heap[parentIndex]
                self.heap[parentIndex] = temp
                
                self._heapifyUp(parentIndex)

    def _heapifyDown(self, index):
        # Time: O(log n)
        # Space: O(1)
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        size = len(self.heap)

        if left < size:
            if self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
                
        if right < size:
            if self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

        if smallest != index:
            # Swap
            temp = self.heap[index]
            self.heap[index] = self.heap[smallest]
            self.heap[smallest] = temp
            
            self._heapifyDown(smallest)

    def insert(self, patientId, severityScore):
        # Time: O(log n)
        # Space: O(n)
        item = (severityScore, patientId)
        self.heap.append(item)
        self._heapifyUp(len(self.heap) - 1)

    def extractMin(self):
        # Time: O(log n)
        # Space: O(n)
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        # Move last element to root
        self.heap[0] = self.heap.pop()
        self._heapifyDown(0)
        return root

    def size(self):
        return len(self.heap)

# --- Hash Table for Patient Index ---
class PatientIndex:
    def __init__(self):
        self.table = {}

    def create(self, patient):
        # Time: O(1)
        # Space: O(m)
        self.table[patient.patientId] = patient
        return True

    def read(self, patientId):
        # Time: O(1)
        # Space: O(1)
        if patientId in self.table:
            return self.table[patientId]
        else:
            return None

    def update(self, patientId, newPatientData):
        # Time: O(1)
        # Space: O(1)
        if patientId in self.table:
            self.table[patientId] = newPatientData
            return True
        return False

    def delete(self, patientId):
        # Time: O(1)
        # Space: O(1)
        if patientId in self.table:
            del self.table[patientId]
            return True
        return False

# --- Stack for Undo Log ---
class UndoStack:
    def __init__(self):
        self.stack = []

    def push(self, action):
        # Time: O(1)
        # Space: O(u)
        self.stack.append(action)

    def pop(self):
        # Time: O(1)
        # Space: O(u)
        if len(self.stack) == 0:
            return None
        return self.stack.pop()

# --- Main System ---
class HospitalSystem:
    def __init__(self):
        self.patientIndex = PatientIndex()
        self.routineQueue = CircularQueue(10) # Fixed size 10
        self.emergencyTriage = MinHeap()
        self.undoLog = UndoStack()
        
        self.doctorSchedules = {}
        self.doctorIndex = {}
        
        self.nextPatientId = 1001
        self.nextTokenId = 1
        self.nextSlotId = 101
        self.servedCount = 0

    def scheduleAddSlot(self, doctorId, startTime, endTime):
        # Time: O(1)
        if doctorId not in self.doctorSchedules:
            self.doctorSchedules[doctorId] = SinglyLinkedList()

        slotId = self.nextSlotId
        self.nextSlotId = self.nextSlotId + 1
        
        schedule = self.doctorSchedules[doctorId]
        schedule.insert(slotId, startTime, endTime, 'FREE')
        return slotId

    def scheduleCancel(self, doctorId, slotId):
        # Time: O(k)
        if doctorId in self.doctorSchedules:
            schedule = self.doctorSchedules[doctorId]
            if schedule.delete(slotId):
                action = ("cancel", doctorId, slotId)
                self.undoLog.push(action)
                return True
        return False

    def registerPatient(self, name, age, severity):
        patientId = self.nextPatientId
        self.nextPatientId = self.nextPatientId + 1
        
        patient = Patient(patientId, name, age, severity)
        self.patientIndex.create(patient)
        
        action = ("register", patientId)
        self.undoLog.push(action)
        return patientId

    def bookAppointment(self, patientId, doctorId):
        patient = self.patientIndex.read(patientId)
        
        if patient is None:
            return "Patient not found."
            
        if doctorId not in self.doctorSchedules:
            return "Doctor not found."

        schedule = self.doctorSchedules[doctorId]
        freeSlot = schedule.findNextFreeSlot()
        
        if freeSlot is None:
            return "No free slots for Doctor " + str(doctorId)

        schedule.updateSlotStatus(freeSlot.slotId, 'BOOKED')
        
        tokenId = self.nextTokenId
        self.nextTokenId = self.nextTokenId + 1
        
        token = Token(tokenId, patientId, doctorId, freeSlot.slotId, 'ROUTINE')

        if self.routineQueue.enqueue(token):
            action = ("book", token.tokenId)
            self.undoLog.push(action)
            return "Routine Appointment booked. Token ID: " + str(tokenId) + ", Slot: " + str(freeSlot.slotId)
        else:
            schedule.updateSlotStatus(freeSlot.slotId, 'FREE')
            return "Booking failed due to queue overflow."

    def emergencyIn(self, patientId, doctorId, severity):
        patient = self.patientIndex.read(patientId)
        if patient is None:
            return "Patient not found. Please register first."

        self.emergencyTriage.insert(patientId, severity)
        
        action = ("triage", patientId, severity)
        self.undoLog.push(action)
        
        return "Emergency Case triaged. Patient ID: " + str(patientId) + ", Severity: " + str(severity)

    def serveNextPatient(self):
        emergencyCase = self.emergencyTriage.extractMin()
        
        if emergencyCase is not None:
            severity = emergencyCase[0]
            patientId = emergencyCase[1]
            
            patient = self.patientIndex.read(patientId)
            self.servedCount = self.servedCount + 1
            
            action = ("serve", patientId, 'EMERGENCY')
            self.undoLog.push(action)
            
            return "Serving EMERGENCY Patient: " + patient.name + " (ID: " + str(patientId) + ")"
        else:
            token = self.routineQueue.dequeue()
            if token is not None:
                patient = self.patientIndex.read(token.patientId)
                
                if token.doctorId in self.doctorSchedules:
                    schedule = self.doctorSchedules[token.doctorId]
                    schedule.updateSlotStatus(token.slotId, 'SERVED')
                    
                self.servedCount = self.servedCount + 1
                
                action = ("serve", token.patientId, 'ROUTINE')
                self.undoLog.push(action)
                
                return "Serving ROUTINE Appointment: " + patient.name + " (Token ID: " + str(token.tokenId) + ")"
            else:
                return "No patients in queue or triage."

    def undoLastAction(self):
        action = self.undoLog.pop()

        if action is None:
            return "No actions to undo."

        actionType = action[0]
        
        if actionType == "book":
            return "Undo for action type 'book' is complex. Logged: " + str(action)
        elif actionType == "serve":
            return "Cannot logically undo serving a patient."
        elif actionType == "register":
            patientId = action[1]
            self.patientIndex.delete(patientId)
            return "Undid Patient Registration for ID: " + str(patientId)
        else:
            return "Undo for this action type is not implemented in basic version."

    def generateReports(self):
        # Using a list to build strings
        lines = []

        lines.append("--- Doctor Schedules and Pending Counts ---")
        
        # Time: O(k) per doctor
        for doctorId in self.doctorSchedules:
            schedule = self.doctorSchedules[doctorId]
            pendingCount = 0
            nextSlot = "N/A"
            
            freeSlot = schedule.findNextFreeSlot()
            if freeSlot is not None:
                nextSlot = "Slot " + str(freeSlot.slotId) + " at " + str(freeSlot.startTime)

            # Using manual loop instead of list comprehension
            all_slots = schedule.traverse()
            for s in all_slots:
                status = s[3] # Index 3 is status
                if status == 'BOOKED':
                    pendingCount = pendingCount + 1

            lines.append("Doctor " + str(doctorId) + ": " + str(pendingCount) + " booked slots. Next Free Slot: " + nextSlot)

        pendingTotal = self.routineQueue.size() + self.emergencyTriage.size()
        lines.append("")
        lines.append("--- Summary ---")
        lines.append("Total Served Patients: " + str(self.servedCount))
        lines.append("Total Pending Patients: " + str(pendingTotal))

        # Joining lines with new line character
        final_report = "\n".join(lines)
        return final_report

    def setupInitialData(self):
        doc1 = Doctor(1, "Dr. Smith", "General")
        doc2 = Doctor(2, "Dr. Jones", "Cardiology")
        
        self.doctorIndex[1] = doc1
        self.doctorIndex[2] = doc2
        
        self.scheduleAddSlot(1, "09:00", "10:00")
        self.scheduleAddSlot(1, "10:00", "11:00")
        self.scheduleAddSlot(2, "09:30", "10:30")
        self.scheduleAddSlot(2, "10:30", "11:30")

    def runCLI(self):
        self.setupInitialData()
        print("")
        print("--- Hospital Appointment & Triage System (CLI) ---")

        while True:
            print("")
            print("Menu:")
            print("1. Register Patient")
            print("2. Book Routine Appointment")
            print("3. Serve Next Patient")
            print("4. Emergency In")
            print("5. Undo Last Action")
            print("6. Reports")
            print("7. Exit")
            
            choice = input("Enter choice: ")

            if choice == '1':
                name = input("Name: ")
                age = input("Age: ")
                severity = input("Default Severity (1-10): ")
                # Converting inputs to int
                pId = self.registerPatient(name, int(age), int(severity))
                print("Registered Patient ID: " + str(pId))
                
            elif choice == '2':
                pId = input("Patient ID: ")
                dId = input("Doctor ID (1 or 2): ")
                result = self.bookAppointment(int(pId), int(dId))
                print(result)
                
            elif choice == '3':
                result = self.serveNextPatient()
                print(result)
                
            elif choice == '4':
                pId = input("Patient ID: ")
                dId = input("Doctor ID: ")
                severity = input("Severity Score (1-10, lower is higher priority): ")
                result = self.emergencyIn(int(pId), int(dId), int(severity))
                print(result)
                
            elif choice == '5':
                result = self.undoLastAction()
                print(result)
                
            elif choice == '6':
                result = self.generateReports()
                print(result)
                
            elif choice == '7':
                print("Exiting System.")
                break
            else:
                print("Invalid choice. Try again.")

app = HospitalSystem()
app.runCLI()
