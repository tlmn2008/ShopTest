# encoding: utf-8


def calc_expected_price(goods, num):
    # 计算商品优惠后的价格
    if type(goods['reduction']) == list:
        # 商品有价格优惠
        if num > len(goods['reduction']):
            # 购买数量大于拥有的优惠数量，取最后一个优惠（应该是最大优惠值）
            redu = goods['reduction'][-1]
        else:
            redu = goods['reduction'][num-1]
        return goods['price'] * num - redu
    elif type(goods['discount']) == list:
        # 商品有折扣优惠
        if num > len(goods['discount']):
            # 购买数量大于拥有的折扣数量，取最后一个折扣（应该是最大折扣值）
            redu = goods['discount'][-1]
        else:
            redu = goods['discount'][num-1]
        return (goods['price'] * num) * redu
    else:
        return False
