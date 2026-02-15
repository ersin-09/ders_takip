
import sys
import unittest
from unittest.mock import MagicMock
import datetime

# Mock tkinter to bypass GUI dependencies
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.font'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.colorchooser'] = MagicMock()
sys.modules['tkinter.simpledialog'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()

# Import the module to be tested
try:
    sys.path.append('.')
    import ders_takip
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

class TestDersTakipLogic(unittest.TestCase):
    def test_kalan_sure_hesapla_ders(self):
        # Calculate times relative to now to avoid mocking datetime
        now = datetime.datetime.now()
        
        # Lesson 1: Starts 10 mins ago, Ends 30 mins from now
        # Currently inside the lesson.
        start1 = (now - datetime.timedelta(minutes=10)).strftime("%H:%M:%S")
        end1 = (now + datetime.timedelta(minutes=30)).strftime("%H:%M:%S")
        
        program = [
            {'Ad': 'Matematik', 'Baslangic': start1, 'Bitis': end1}
        ]
        
        result = ders_takip.kalan_süre_hesapla(program)
        
        # We expect it to be DERS type
        self.assertEqual(result['Type'], 'DERS', f"Expected DERS, got {result['Type']}")
        self.assertEqual(result['Ad'], 'Matematik')
        
        # Expected remaining seconds: roughly 30 * 60 = 1800
        # Allow some margin for execution time (e.g., +/- 2 seconds)
        expected_seconds = 30 * 60
        self.assertTrue(abs(result['Kalan_Saniye'] - expected_seconds) < 5, 
                        f"Expected approx {expected_seconds}, got {result['Kalan_Saniye']}")

    def test_kalan_sure_hesapla_teneffus(self):
        now = datetime.datetime.now()
        
        # Lesson 1: Ended 5 mins ago
        start1 = (now - datetime.timedelta(minutes=45)).strftime("%H:%M:%S")
        end1 = (now - datetime.timedelta(minutes=5)).strftime("%H:%M:%S")
        
        # Lesson 2: Starts 5 mins from now
        start2 = (now + datetime.timedelta(minutes=5)).strftime("%H:%M:%S")
        end2 = (now + datetime.timedelta(minutes=45)).strftime("%H:%M:%S")
        
        program = [
            {'Ad': 'Matematik', 'Baslangic': start1, 'Bitis': end1},
            {'Ad': 'Fizik', 'Baslangic': start2, 'Bitis': end2}
        ]
        
        result = ders_takip.kalan_süre_hesapla(program)
        
        self.assertEqual(result['Type'], 'TENEFFÜS', f"Expected TENEFFÜS, got {result['Type']}")
        # In break, Ad is None
        self.assertIsNone(result['Ad'])
        
        # Expected remaining seconds: 5 * 60 = 300
        expected_seconds = 5 * 60
        self.assertTrue(abs(result['Kalan_Saniye'] - expected_seconds) < 5,
                        f"Expected approx {expected_seconds}, got {result['Kalan_Saniye']}")

if __name__ == '__main__':
    unittest.main()
