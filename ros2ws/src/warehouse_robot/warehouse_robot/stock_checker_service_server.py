import rclpy
from rclpy.node import Node
from my_interface.srv import CheckStock

class StockCheckerServiceServer(Node):
    def __init__(self):
        super().__init__('stock_checker_service_server')
        self.srv = self.create_service(CheckStock, 'check_stock', self.check_stock_callback)
        self.stock = {'item1': 10, 'item2': 5, 'item3': 0}  # Example stock levels

    def check_stock_callback(self, request, response):
        self.get_logger().info(f'Received stock check request for {request.item_name}')
        item_name = request.item_name
        if item_name in self.stock:
            response.stock_level = self.stock[item_name]
            self.get_logger().info(f'Stock check request: {item_name} - Stock level: {response.stock_level}')
        else:
            response.stock_level = 0
            self.get_logger().info(f'Item {item_name} not found')
        return response

def main(args=None):
    rclpy.init(args=args)
    service_server = StockCheckerServiceServer()
    rclpy.spin(service_server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
