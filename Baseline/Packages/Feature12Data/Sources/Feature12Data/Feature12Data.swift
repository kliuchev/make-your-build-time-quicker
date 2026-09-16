import Feature12Domain

public enum Feature12DataRepository {
    public static func load(_ id: Int) -> Feature12DomainModel {
        Feature12DomainModel(id: id, title: "Feature 12")
    }
}
