from auctions.application.repositories import AuctionsRepository
from auctions.domain.entities import (
    Auction,
    Bid,
)
from auctions.domain.factories import get_dollars


class DjangoORMAuctionsRepository(AuctionsRepository):

    def get(self, auction_id: int) -> Auction:
        from auctions.models import Auction as AuctionModel

        auction_model = AuctionModel.objects.prefetch_related('bid_set').get(id=auction_id)
        return Auction(
            id=auction_model.id,
            title=auction_model.title,
            initial_price=get_dollars(auction_model.initial_price),
            bids=[
                Bid(id=bid_model.id, bidder_id=bid_model.bidder_id, amount=get_dollars(bid_model.amount))
                for bid_model in auction_model.bid_set.all()
            ]
        )

    def save(self, auction: Auction) -> None:
        from auctions.models import (
            Auction as AuctionModel,
            Bid as BidModel
        )

        model = AuctionModel(
            id=auction.id,
            title=auction.title,
            initial_price=auction.initial_price.amount,
            current_price=auction.current_price.amount
        )
        model.save()
        new_bids = [bid for bid in auction.bids if not bid.id]
        for bid in new_bids:
            BidModel.objects.create(
                auction_id=model.id,
                bidder_id=bid.bidder_id,
                amount=bid.amount.amount
            )
        if auction.withdrawn_bids_ids:
            BidModel.objects.filter(id__in=auction.withdrawn_bids_ids).delete()
