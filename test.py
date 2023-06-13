# import shopify

# access_token = "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"
# shop_url = "livaroom.myshopify.com"

# api_version = '2023-01'
# session = shopify.Session(shop_url, api_version, access_token)
# shopify.ShopifyResource.activate_session(session)

# import requests
# import json

# url = 'https://your-shops-name.myshopify.com/admin/api/2022-01/graphql.json'
# headers = {"Content-Type": "application/graphql",
#            "X-Shopify-Access-Token": YOUR_ACCESS_TOKEN}

# request = requests.post(url, data=your_query, headers=headers)
# print(json.loads(request.text))



# import shopify

# access_token = "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"
# shop_url = "livaroom.myshopify.com"

# api_version = '2023-01'
# session = shopify.Session(shop_url, api_version, access_token)
# shopify.ShopifyResource.activate_session(session)

# query = """
# query {
#   products(first: 10) {
#     edges {
#       node {
#         handle
#         id
#         description
#       }
#     }
#   }
# }
# """

# r = shopify.GraphQL().execute(query)
# print(r)

# import shopify
# import json

# access_token = "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"
# shop_url = "livaroom.myshopify.com"
# api_version = '2023-01'

# session = shopify.Session(shop_url, api_version, access_token)
# shopify.ShopifyResource.activate_session(session)

# variants = [
#     {"id": 44182936158515, "price": "380"},
#     # Add more variant IDs and prices as needed
# ]


# mutation_query = """
# mutation productVariantUpdate($input: ProductVariantInput!) {
#   productVariantUpdate(input: $input) {
#     productVariant {
#       id
#       price
#     }
#   }
# }
# """


# for variant in variants:
#     variant_id = variant["id"]
#     variant_price = variant["price"]

#     variables = {
#         "input": {
#             "id": variant_id,
#             "price": variant_price
#         }
#     }

#     r = shopify.GraphQL().execute(mutation_query, variables=json.dumps(variables))
#     print(r.decode("utf-8"))


import shopify
import json

access_token = "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"
shop_url = "livaroom.myshopify.com"
api_version = '2023-01'

session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)


variants = [
    {"id": "gid://shopify/ProductVariant/44182936158515", "price": "380"},
    # Add more variant IDs and prices as needed
]

mutation_query = """
mutation productVariantUpdate($input: ProductVariantInput!) {
  productVariantUpdate(input: $input) {
    productVariant {
      id
      title
      price
    }
  }
}
"""

for variant in variants:
    variant_id = variant["id"]
    variant_price = variant["price"]

    variables = {
        "input": {
            "id": variant_id,
            "price": variant_price
        }
    }

    r = shopify.GraphQL().execute(mutation_query, variables=variables)
    print(r)
