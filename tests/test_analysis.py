import unittest

from src.analysis import summarize_sales


class SummarizeSalesTests(unittest.TestCase):
	def test_summarizes_normal_dataset(self):
		records = [
			{"Order_id": 1, "Revenue": 100.0, "Category": "Electronics"},
			{"Order_id": 2, "Revenue": 200.0, "Category": "Clothing"},
			{"Order_id": 3, "Revenue": 150.0, "Category": "Electronics"},
		]

		summary = summarize_sales(records)

		self.assertEqual(
			summary,
			{
				"total_revenue": 450.0,
				"number_of_orders": 3,
				"avg_order_value": 150.0,
				"revenue_by_category": {
					"Electronics": 250.0,
					"Clothing": 200.0,
				},
				"missing_revenue_count": 0,
				"negative_revenue_count": 0,
				"negative_revenue": 0,
				"missing_category_count": 0,
			},
		)

	def test_returns_message_for_empty_input(self):
		self.assertEqual(summarize_sales([]), "No records found")

	def test_multiple_categories(self):
		records = [
			{"Order_id": 1, "Revenue": 80.0, "Category": "Electronics"},
			{"Order_id": 2, "Revenue": 120.0, "Category": "Clothing"},
		]

		summary = summarize_sales(records)

		self.assertGreater(len(summary["revenue_by_category"]), 1)


if __name__ == "__main__":
	unittest.main()
