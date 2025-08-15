const DB_NAME = process.env.MONGO_INITDB_DATABASE;

db = db.getSiblingDB(DB_NAME);

use ad_platform;

db.createCollection("sessions", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["UserID", "Device", "SessionStart", "SessionEnd", "Impressions"],
      properties: {
        UserID: { bsonType: "string" },
        Device: { bsonType: "string" },
        SessionStart: { bsonType: "date" },
        SessionEnd: { bsonType: "date" },

        Impressions: {
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

