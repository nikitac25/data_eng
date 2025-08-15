const DB_NAME = process.env.MONGO_INITDB_DATABASE;

db = db.getSiblingDB(DB_NAME);

db.createCollection("user_stats", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["UserID", "demographics", "engagements"],
      properties: {
        UserID: { bsonType: "string" },
        demographics: {
          bsonType: "object",
          required: ["Age", "Gender", "Location", "Interests", "SignupDate"],
          properties: {
            Age: { bsonType: ["int", "long", "double", "decimal"] },
            Gender: { bsonType: "string" },
            Location: { bsonType: "string" },
            Interests: {
              oneOf: [
                { bsonType: "string" },
                { bsonType: "array", items: { bsonType: "string" } }
              ]
            },
            SignupDate: { bsonType: "date" }
          }
        },
        engagements: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["EventID", "Timestamp", "AdvertiserName", "CampaignName"],
            properties: {
              EventID: { bsonType: "string" },
              AdvertiserName: { bsonType: "string" },
              CampaignName: { bsonType: "string" },
              CampaignStartDate: { bsonType: "date" },
              CampaignEndDate: { bsonType: "date" },
              CampaignTargetingCriteria: { bsonType: "string" },
              CampaignTargetingInterest: { bsonType: "string" },
              CampaignTargetingCountry: { bsonType: "string" },
              AdSlotSize: { bsonType: "string" },
              UserID: { bsonType: "string" },
              Device: { bsonType: "string" },
              Location: { bsonType: "string" },
              Timestamp: { bsonType: "date" },
              BidAmount: { bsonType: ["double", "decimal", "int", "long"] },
              AdCost: { bsonType: ["double", "decimal", "int", "long"] },
              AdRevenue: { bsonType: ["double", "decimal", "int", "long"] },
              Budget: { bsonType: ["double", "decimal", "int", "long"] },
              RemainingBudget: { bsonType: ["double", "decimal", "int", "long"] },
              Clicks: {
                bsonType: "array",
                items: {
                  bsonType: "object",
                  properties: {
                    WasClicked: { bsonType: "bool" },
                    ClickTimestamp: { bsonType: "date" }
                  },
                  additionalProperties: false
                }
              }
            },
            additionalProperties: false
          }
        }
      },
      additionalProperties: false
    }
  }
});
