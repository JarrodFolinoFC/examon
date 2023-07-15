from collections import Counter


class Stats:
    @staticmethod
    def calc_stats(questions):
        return {
            'total_questions': len(questions),
            'tags_summary': Stats.uniq_tags(questions),
            'tags': Stats.tag_count(questions),
        }

    @staticmethod
    def tag_count(questions):
        counter = Counter()
        for q in questions:
            counter.update(q.tags)

        return counter

    @staticmethod
    def uniq_tags(questions):
        tag_set = set()
        [[tag_set.add(tag) for tag in q.tags] for q in questions]
        return list(tag_set)
