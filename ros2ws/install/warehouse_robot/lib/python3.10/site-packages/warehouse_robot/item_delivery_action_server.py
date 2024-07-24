import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from my_interface.action import DeliverItem
from warehouse_robot.stock_checker_service_client import StockCheckerServiceClient

class ItemDeliveryActionServer(Node):
    def __init__(self):
        super().__init__('item_delivery_action_server')
        self._action_server = ActionServer(
            self,
            DeliverItem,
            'deliver_item',
            self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            handle_accepted_callback=self.handle_accepted_callback
        )
        self._stock_checker_client = StockCheckerServiceClient()
        
    def goal_callback(self, goal_request):
        item_name = goal_request.item_name
        quantity = goal_request.quantity
        self.get_logger().info(f'Received delivery request: {item_name} x {quantity}')
        
        time.sleep(1)

        stock_level = self._stock_checker_client.send_request(item_name)
        
        if stock_level is None:
            self.get_logger().info(f'Failed to check stock for {item_name}')
            return GoalResponse.REJECT
        
        self.get_logger().info(f'Stock level for {item_name}: {stock_level}')
        
        if stock_level <= 0:
            self.get_logger().info(f'Item {item_name} not available')
            return GoalResponse.REJECT
        
        if stock_level < quantity:
            self.get_logger().info(f'Insufficient stock Item: {item_name}')
            return GoalResponse.REJECT
        
        return GoalResponse.ACCEPT
    
    def cancel_callback(self, goal_handle):
        self.get_logger().info('Cancel request')
        return CancelResponse.ACCEPT
        
    def handle_accepted_callback(self, goal_handle):
        self.get_logger().info('Goal accepted...')
        goal_handle.execute()

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Execute callback ...')
        
        feedback_msg = DeliverItem.Feedback()
        feedback_msg.status = 'Delivering...'
        goal_handle.publish_feedback(feedback_msg)

        # Simulate delivery process
        self.get_logger().info('Delivering...')
        for i in range(5):
            feedback_msg.status = f'Delivery progress: {i*20}%'
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Delivery progress: {i*20}%')
            time.sleep(1)
            
        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            result = DeliverItem.Result()
            result.success = False
            result.message = 'Cancel delivery ...'
            goal_handle.publish_feedback(feedback_msg)
            return result

        goal_handle.succeed()
        result = DeliverItem.Result()
        result.success = True
        result.message = f'Delivered {goal_handle.request.item_name} x {goal_handle.request.quantity}'
        self.get_logger().info(result.message)
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = ItemDeliveryActionServer()
    rclpy.spin(action_server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
