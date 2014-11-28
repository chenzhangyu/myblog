from .. import db
from tags import Tags

_passage = db.Passages()
_tag = Tags()


class Passages(db.Passages):
    """A wrapper class for oprations on table passages"""
    
    def set_tags(self, tag_list):
        for t in self.tags.all():
            super(Passages, self).pas_tag.remove(t)
        for tag in tag_list:
            # assert Tags.is_registered(tag), \
            #         "attempt to delete a invalid tag :%r" % tag
            super(Passages, self).pas_tag.append(_tag.query.filter_by(tag=tag).first())
