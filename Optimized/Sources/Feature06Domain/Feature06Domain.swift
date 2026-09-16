import Shared

public struct Feature06DomainModel: Sendable {
    public let id: Int
    public let title: String

    public init(id: Int, title: String) {
        self.id = id
        self.title = title
    }

    public var score: Int { SharedScore.value(id) + 6 }
}
