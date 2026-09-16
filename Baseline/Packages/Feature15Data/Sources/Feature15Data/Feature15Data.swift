import Feature15Domain

public enum Feature15DataRepository {
    public static func load(_ id: Int) -> Feature15DomainModel {
        Feature15DomainModel(id: id, title: "Feature 15")
    }
}
