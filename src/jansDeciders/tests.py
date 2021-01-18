#!/usr/bin/python3

import unittest, subprocess

class TestE2E(unittest.TestCase):
  def testLogStarDeciderProblem1(self):
    result = subprocess.run(['./log_star_decider.py'], input=b"111", capture_output=True)
    lines = str(result.stdout.decode('utf-8')).split('\n')

    self.assertEqual(len(lines), 2)
    self.assertEqual(lines[0], "O(log*n)")
    self.assertEqual(lines[1], "")

  def testLogStarDeciderProblem2(self):
    result = subprocess.run(['./log_star_decider.py'], input=b"121 123 212 131 323 454", capture_output=True)
    lines = str(result.stdout.decode('utf-8')).split('\n')

    self.assertEqual(len(lines), 2)
    self.assertEqual(lines[0], "O(log*n)")
    self.assertEqual(lines[1], "")

  def testLogStarDeciderProblem3(self):
    result = subprocess.run(['./log_star_decider.py'], input=b"454", capture_output=True)
    lines = str(result.stdout.decode('utf-8')).split('\n')

    self.assertEqual(len(lines), 2)
    self.assertEqual(lines[0], "ω(log*n)")
    self.assertEqual(lines[1], "")

  def testLogStarDeciderProblem4(self):
    result = subprocess.run(['./log_star_decider.py'], input=b"1M1 010 M11 M01", capture_output=True)
    lines = str(result.stdout.decode('utf-8')).split('\n')

    self.assertEqual(len(lines), 2)
    self.assertEqual(lines[0], "O(log*n)")
    self.assertEqual(lines[1], "")

  def testLogStarDeciderProblem5(self):
    result = subprocess.run(['./log_star_decider.py'], input=b"121 112 212", capture_output=True)
    lines = str(result.stdout.decode('utf-8')).split('\n')

    self.assertEqual(len(lines), 2)
    self.assertEqual(lines[0], "ω(log*n)")
    self.assertEqual(lines[1], "")

  def testLogStarDeciderProblem6(self):
    result = subprocess.run(['./log_star_decider.py'], input=b"212 122 111", capture_output=True)
    lines = str(result.stdout.decode('utf-8')).split('\n')

    self.assertEqual(len(lines), 2)
    self.assertEqual(lines[0], "O(log*n)")
    self.assertEqual(lines[1], "")

  def testLogDecider1(self):
    result = subprocess.run(['./log_decider.py'], input=b"111", capture_output=True)
    lines = str(result.stdout.decode('utf-8')).split('\n')

    self.assertEqual(len(lines), 2)
    self.assertEqual(lines[0], "O(log n)")
    self.assertEqual(lines[1], "")

  def testLogDecider2(self):
    result = subprocess.run(['./log_decider.py'], input=b"121 212", capture_output=True)
    lines = str(result.stdout.decode('utf-8')).split('\n')

    self.assertEqual(len(lines), 2)
    self.assertEqual(lines[0], "Ω(n)")
    self.assertEqual(lines[1], "")

