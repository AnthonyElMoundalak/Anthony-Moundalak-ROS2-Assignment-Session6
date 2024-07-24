import rclpy
from rclpy.node import Node
from my_interface.srv import CheckStock

class StockCheckerServiceClient(Node):
    def __init__(self):
        super().__init__('stock_checker_service_client')
        self.cli = self.create_client(CheckStock, 'check_stock')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = CheckStock.Request()

    def send_request(self, item_name):
        self.get_logger().info(f'Sending request for stock level of {item_name}')
        self.req.item_name = item_name
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        self.get_logger().info('Send request for the stock client...')
        if self.future.result() is None:
            self.get_logger().error('Service call failed')
            return None
        self.response = self.future.result()
        self.get_logger().info(f'Stock level: {self.response.stock_level}')
        self.get_logger().info(f'Received response: Stock level for {item_name} is {self.response.stock_level}')
        return self.response.stock_level


def main(args=None):
    rclpy.init(args=args)
    service_client = StockCheckerServiceClient()
    # response = service_client.send_request('item1')
    # service_client.get_logger().info(f'Stock level for item1: {response.stock_level}')
    # rclpy.shutdown()
    try:
        rclpy.spin(service_client)
    except KeyboardInterrupt:
        pass
    finally:
        service_client.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
